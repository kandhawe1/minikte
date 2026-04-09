from brokers.zerodha_adapter import ZerodhaAdapter
from brokers.fyers_adapter import FyersAdapter


class BrokerFactory:

    @staticmethod
    def get_broker(broker_name: str):

        if broker_name.lower() == "zerodha":
            return ZerodhaAdapter()

        if broker_name.lower() == "fyers":
            return FyersAdapter()

        raise Exception("Unsupported broker")