from brokers.broker_interface import BrokerInterface
import asyncio


class AngeloneAdapter(BrokerInterface):

    async def authenticate(self, credentials):
        print("Authenticated with Angelone")

    async def place_order(self, symbol, quantity, side):
        await asyncio.sleep(0.5)
        return {
            "symbol": symbol, "status": "SUCCESS", "message": f"{side} order executed for {quantity}"
        }

    async def get_holdings(self):
        return []