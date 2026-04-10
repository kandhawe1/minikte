from brokers.broker_interface import BrokerInterface
from SmartApi import SmartConnect
import pyotp
import asyncio
from core.instrument_master import InstrumentMaster
from core.risk_manager import RiskManager


class AngeloneAdapter(BrokerInterface):

    def __init__(self):
        self.client = None

        self.jwt_token = None
        self.refresh_token = None
        self.api_key = None
        self.credentials = None

        self.instrument_master = InstrumentMaster()
        self.risk = RiskManager()

        self.instrument_master.load()

        # 🔥 CRITICAL: prevents SmartConnect race conditions
        self.global_lock = asyncio.Lock()

    # =========================================================
    # UTIL
    # =========================================================

    def is_token_error(self, error):
        return "Invalid Token" in str(error) or "AG8001" in str(error)

    def _create_client(self):
        self.client = SmartConnect(api_key=self.api_key)

    # =========================================================
    # AUTH
    # =========================================================

    async def authenticate(self, credentials):

        async with self.global_lock:

            self.credentials = credentials
            self.api_key = credentials["api_key"]

            self._create_client()

            totp = pyotp.TOTP(credentials["totp_secret"]).now()

            data = self.client.generateSession(
                credentials["client_code"],
                credentials["mpin"],
                totp
            )

            if not data.get("status"):
                raise Exception(f"Login failed: {data}")

            self.jwt_token = data["data"]["jwtToken"]
            self.refresh_token = data["data"]["refreshToken"]

            self.client.setAccessToken(self.jwt_token)

            print("✅ AUTH SUCCESS")

    # =========================================================
    # RESET SESSION
    # =========================================================

    async def reset_session(self):

        async with self.global_lock:

            print("🔄 HARD RESET SESSION")

            self._create_client()

            totp = pyotp.TOTP(self.credentials["totp_secret"]).now()

            data = self.client.generateSession(
                self.credentials["client_code"],
                self.credentials["mpin"],
                totp
            )

            if not data.get("status"):
                raise Exception(f"Reset failed: {data}")

            self.jwt_token = data["data"]["jwtToken"]
            self.refresh_token = data["data"]["refreshToken"]

            self.client.setAccessToken(self.jwt_token)

            print("✅ SESSION RESET DONE")

    # =========================================================
    # SAFE CALL ENGINE
    # =========================================================

    async def safe_call(self, func, *args, retry=True):

        async with self.global_lock:

            loop = asyncio.get_event_loop()

            def call():
                return func(*args)

            try:
                return await loop.run_in_executor(None, call)

            except Exception as e:

                if retry and self.is_token_error(e):

                    print("⚠️ Token expired → recovering session")

                    await self.reset_session()

                    return await loop.run_in_executor(None, call)

                raise

    # =========================================================
    # FUNDS (ONLY SMARTCONNECT)
    # =========================================================

    async def get_funds(self):
        response = await self.safe_call(self.client.rmsLimit)
        return response["data"]

    # =========================================================
    # HOLDINGS
    # =========================================================

    async def get_holdings(self):
        response = await self.safe_call(lambda: self.client.holding())
        return response["data"]

    # =========================================================
    # POSITIONS
    # =========================================================

    async def get_positions(self):
        response = await self.safe_call(lambda: self.client.position())
        return response["data"]

    # =========================================================
    # SMART RISK ENGINE (NO REST MARGIN API)
    # =========================================================

    async def estimate_margin(self, symbol, quantity, price=100):

        """
        Since SmartAPI does NOT expose margin API in SDK,
        we estimate margin conservatively.
        """

        # crude intraday estimate (typical broker leverage ~5x–10x)
        estimated_trade_value = quantity * price

        leverage = 5  # conservative intraday leverage assumption

        required_margin = estimated_trade_value / leverage

        return {
            "estimated_margin": required_margin,
            "estimated_trade_value": estimated_trade_value
        }

    # =========================================================
    # PLACE ORDER
    # =========================================================

    async def place_order(self, symbol, quantity, side):

        try:

            symbol_token = self.instrument_master.get_token(symbol)

            # 🔥 get live funds (SmartConnect only)
            funds = await self.get_funds()
            available_funds = float(funds["availablecash"])

            # fallback price assumption (you can replace with LTP API later)
            estimated_price = 100

            margin = await self.estimate_margin(symbol, quantity, estimated_price)

            required_margin = margin["estimated_margin"]

            if required_margin > available_funds:
                return {
                    "symbol": symbol,
                    "status": "FAILED",
                    "reason": "Insufficient funds",
                    "required_margin": required_margin,
                    "available_funds": available_funds
                }

            orderparams = {
                "variety": "NORMAL",
                "tradingsymbol": symbol,
                "symboltoken": symbol_token,
                "transactiontype": side,
                "exchange": "NSE",
                "ordertype": "MARKET",
                "producttype": "INTRADAY",
                "duration": "DAY",
                "quantity": quantity
            }

            api_response = await self.safe_call(
                self.client.placeOrder,
                orderparams
            )

            order_id = None
            if isinstance(api_response, dict):
                order_id = api_response.get("data", {}).get("orderid")

            return {
                "symbol": symbol,
                "status": "SUCCESS",
                "order_id": order_id or api_response,
                "estimated_margin": required_margin
            }

        except Exception as e:
            return {
                "symbol": symbol,
                "status": "FAILED",
                "error": str(e)
            }