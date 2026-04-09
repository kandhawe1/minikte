from abc import ABC, abstractmethod


class BrokerInterface(ABC):

    @abstractmethod
    async def authenticate(self, credentials):
        pass

    @abstractmethod
    async def place_order(self, symbol, quantity, side):
        pass

    @abstractmethod
    async def get_holdings(self):
        pass