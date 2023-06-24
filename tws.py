import threading
import time
import pandas as pd
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract, BarData


class MyWrapper(EWrapper):
    def __init__(self):
        self.dfs = {}
        self.symbols = ["EURUSD", "GBPUSD", "USDCHF", "USDCAD",
                        "USDJPY", "EURJPY", "GBPJPY", "CHFJPY", "AUDUSD", "NZDUSD"]
        self.timeframes = ["5 mins", "15 mins", "1 hour",
                           "4 hours", "1 day", "1 week", "1 month"]
        self.subscription_ids = {}
        self.connection_status = False

    def nextValidId(self, orderId: int):
        for symbol in self.symbols:
            for timeframe in self.timeframes:
                self.request_historical_data(symbol, timeframe)

    def request_historical_data(self, symbol, timeframe):
        subscription_id = len(self.subscription_ids) + 1

        # Crear contrato para el par de divisas
        contract = Contract()
        contract.symbol = symbol[:3]
        contract.secType = "CASH"
        contract.currency = symbol[3:]
        contract.exchange = "IDEALPRO"

        self.reqHistoricalData(subscription_id, contract, "",
                               timeframe, "1 month", "MIDPOINT", 0, 1, False, [])

        key = f"{symbol}_{timeframe}"
        self.subscription_ids[subscription_id] = key
        self.dfs[key] = pd.DataFrame(
            columns=["Date", "Open", "High", "Low", "Close"])

    def historicalData(self, reqId: int, bar: BarData):
        key = self.subscription_ids[reqId]
        df = self.dfs[key]

        df = df.append({"Date": bar.date, "Open": bar.open, "High": bar.high, "Low": bar.low, "Close": bar.close},
                       ignore_index=True)

        self.dfs[key] = df

    def check_subscription_status(self):
        if len(self.subscription_ids) == len(self.symbols) * len(self.timeframes):
            print("Todas las suscripciones están activas y autorizadas.")
        else:
            print("No todas las suscripciones están activas o autorizadas.")

    def set_connection_status(self, status):
        self.connection_status = status


class SubscriptionThread(threading.Thread):
    def __init__(self, wrapper, symbol, timeframe):
        threading.Thread.__init__(self)
        self.wrapper = wrapper
        self.symbol = symbol
        self.timeframe = timeframe

    def run(self):
        while True:
            if not self.wrapper.connection_status:
                break

            key = f"{self.symbol}_{self.timeframe}"
            if key in self.wrapper.subscription_ids.values():
                time.sleep(5)
            else:
                self.wrapper.request_historical_data(
                    self.symbol, self.timeframe)
                time.sleep(1)


def main():
    app = EClient(MyWrapper())

    threads = []
    for symbol in app.wrapper.symbols:
        for timeframe in app.wrapper.timeframes:
            thread = SubscriptionThread(app.wrapper, symbol, timeframe)
            thread.start()
            threads.append(thread)

    while True:
        try:
            app.connect("127.0.0.1", 7497, clientId=1)
            app.wrapper.set_connection_status(True)
            app.run()
            app.disconnect()
            app.wrapper.set_connection_status(False)
            break
        except ConnectionRefusedError:
            print(
                "No se puede establecer una conexión con TWS. Esperando 1 minuto para reconectarse...")
            time.sleep(60)

    # Imprimir el estado de las suscripciones
    app.wrapper.check_subscription_status()

    # Esperar a que todos los hilos de suscripción finalicen
    for thread in threads:
        thread.join()

    # Guardar los datos en un archivo Excel
    with pd.ExcelWriter("precios_divisas.xlsx") as writer:
        for key, df in app.wrapper.dfs.items():
            symbol, timeframe = key.split("_")
            sheet_name = f"{symbol}_{timeframe}"
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print("Proceso completado.")


if __name__ == "__main__":
    main()
