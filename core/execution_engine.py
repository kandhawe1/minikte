import asyncio
from core.order_manager import OrderManager


class ExecutionEngine:

    def __init__(self, broker):
        self.broker = broker
        self.holdings = {}   # internal holdings store
        self.order_manager = OrderManager(broker)

    async def load_holdings(self):
        """
        Load holdings from broker only once
        """
        broker_holdings = await self.broker.get_holdings()

        for h in broker_holdings:
            self.holdings[h["symbol"]] = h["quantity"]

    def update_holdings(self, symbol, quantity, action):
        """
        Update internal holdings after each trade
        """

        current = self.holdings.get(symbol, 0)

        if action == "BUY":
            self.holdings[symbol] = current + quantity

        elif action == "SELL":
            new_qty = current - quantity

            if new_qty == 0:
                self.holdings.pop(symbol, None)
            else:
                self.holdings[symbol] = new_qty

    async def execute_portfolio(self, orders):

        results = []

        # Load broker holdings only first time
        if not self.holdings:
            await self.load_holdings()

        # FIRST TIME PORTFOLIO
        if not self.holdings:
            print("First-time portfolio detected")

            for order in orders:
                current_qty = self.holdings.get(order.symbol, 0)

                # REBALANCE
                if order.action == "SELL" and order.quantity <= 0:
                    message = f"{order.symbol} - Qty -ve not allowed, please use REBALANCE"
                    print(message)

                    results.append({
                        "symbol": order.symbol, "status": "FAILED", "message": message
                    })
                    continue

                # REBALANCE
                if order.action == "REBALANCE" and current_qty <= 0 and order.quantity <= 0:
                    message = f"{order.symbol} - No holdings to SELL"
                    print(message)

                    results.append({
                        "symbol": order.symbol, "status": "FAILED", "message": message
                    })
                    continue

                result = await self.broker.place_order( order.symbol, order.quantity, order.action )
                self.update_holdings(order.symbol, order.quantity, order.action)
                results.append(result)

        # REBALANCING
        else:
            print("Rebalancing portfolio")

            for order in orders:
                symbol = order.symbol
                action = order.action
                qty = order.quantity

                if action == "REBALANCE":

                    if qty > 0:
                        action = "BUY"
                    else:
                        action = "SELL"
                        qty = abs(qty)


                if order.action == "SELL" and order.quantity <= 0:
                    message = f"{order.symbol} - Qty -ve not allowed, please use REBALANCE"
                    print(message)

                    results.append({
                        "symbol": order.symbol, "status": "FAILED", "message": message
                    })
                    continue


                result = await self.broker.place_order(symbol,qty,action)
                self.update_holdings(order.symbol, qty, action)
                results.append(result)

        print("Updated Holdings:", self.holdings)

        return results