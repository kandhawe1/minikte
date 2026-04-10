class RiskManager:

    def validate(self, quantity):

        if quantity > 1000:
            raise Exception("Risk limit exceeded")

        return True