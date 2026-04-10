import requests


class InstrumentMaster:

    def __init__(self):
        self.instruments = {}

    def load(self):

        url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"

        data = requests.get(url).json()

        for item in data:
            symbol = item["symbol"]
            token = item["token"]

            self.instruments[symbol] = token

    def get_token(self, symbol):

        return self.instruments.get(symbol)