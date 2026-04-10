from brokers.zerodha_adapter import ZerodhaAdapter
from brokers.fyers_adapter import FyersAdapter
from brokers.angelone_adapter import AngeloneAdapter
from brokers.groww_adapter import GrowwAdapter
from brokers.upstox_adapter import UpstoxAdapter


class BrokerFactory:

    brokers = {
        "zerodha": ZerodhaAdapter,
        "fyers": FyersAdapter,
        "angelone": AngeloneAdapter,
        "groww": GrowwAdapter,
        "upstox": UpstoxAdapter
    }

    @classmethod
    def get_broker(cls, broker_name):

        broker_class = cls.brokers.get(broker_name)

        if not broker_class:
            raise Exception("Unsupported broker")

        return broker_class()