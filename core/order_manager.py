import asyncio


class OrderManager:

    def __init__(self, broker):
        self.broker = broker

    async def execute_order(self, order):

        try:
            result = await self.broker.place_order(
                symbol=order.symbol,
                quantity=order.quantity,
                side=order.action
            )

            return result

        except Exception as e:

            return {
                "symbol": order.symbol,
                "status": "FAILED",
                "message": str(e)
            }