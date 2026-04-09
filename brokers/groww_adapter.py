from brokers.broker_interface import BrokerInterface
import asyncio


class GrowwAdapter(BrokerInterface):
    async def authenticate(self, credentials):
        print("Authenticated with Groww")

    async def place_order(self, symbol, quantity, side):
        await asyncio.sleep(0.5)
        return {
            "symbol": symbol, "status": "SUCCESS", "message": f"{side} order executed for {quantity}"
        }

    async def get_holdings(self):
        return []