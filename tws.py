from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper
import csv
import time


class MyWrapper(EWrapper):
    def __init__(self):
        self.csv_file = None
        self.csv_writer = None
        self.client = None

    def historicalData(self, reqId, bar):
        if self.csv_writer is not None:
            self.csv_writer.writerow([bar.date, bar.time, bar.close])

    def connectionClosed(self):
        print("Se perdió la conexión con la API. Intentando reconectar...")

        # Cerrar el archivo CSV
        if self.csv_file is not None:
            self.csv_file.close()

        while not self.client.isConnected():
            try:
                # Esperar 15 segundos antes de intentar reconectar
                time.sleep(15)

                # Reconectar
                self.client.connect("127.0.0.1", 7497, 0)
            except Exception as e:
                print(f"Error al reconectar: {str(e)}")


def main():
    # Crear una instancia de EClient y MyWrapper
    wrapper = MyWrapper()
    client = EClient(wrapper)
    wrapper.client = client

    # Conectar a la API de TWS o IB Gateway
    client.connect("127.0.0.1", 7497, 0)

    # Crear y configurar el objeto Contract para el USD
    contract = Contract()
    contract.symbol = "USD"
    contract.secType = "CASH"
    contract.exchange = "IDEALPRO"
    contract.currency = "USD"

    while True:
        # Crear un archivo CSV
        csv_file = open("datos.csv", mode="w", newline="")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Fecha", "Hora", "Precio de Cierre"])

        # Asignar el archivo CSV al wrapper
        wrapper.csv_file = csv_file
        wrapper.csv_writer = csv_writer

        # Solicitar datos históricos en temporalidad de 1 minuto
        client.reqHistoricalData(
            1, contract, "", "1 D", "1 min", "BID_ASK", 1, 1, False, [])

        # Esperar a que se reciban los datos históricos
        client.run()

        # Cerrar el archivo CSV
        csv_file.close()

    # Desconectar de la API de TWS o IB Gateway
    client.disconnect()


if __name__ == "__main__":
    main()
