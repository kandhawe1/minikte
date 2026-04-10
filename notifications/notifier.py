class Notifier:

    def notify(self, results):

        print("Trade Execution Summary")

        for r in results:

            print(
                f"Symbol: {r['symbol']} "
                f"Status: {r['status']} "
                f"Message: {r.get('message') or r.get('error') or 'N/A'}"
            )