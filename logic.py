from PyQt6.QtWidgets import *
import api
from gui import *
from polygon import RESTClient
import requests


class Logic(QMainWindow, Ui_Dashboard):
    API = api.Polygon.API

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.buy_pushButton.clicked.connect(lambda: self.buy())
        self.sell_pushButton.clicked.connect(lambda: self.sell())
        self.clear_entries_pushButton.clicked.connect(lambda: self.clear())
        self.client = RESTClient(api_key=Logic.API)
        self.init_table()

    def buy(self) -> None:
        """

        :return: None. This method should perform validation at beginning & if succesfull
        it should add the update the Table on the GUI with the Symbol, Quantity, & Price info (pulled from API).

        """
        if not self.validate():
            return

        price = self.get_data()
        row = self.positions_table.rowCount()
        self.positions_table.insertRow(row)
        self.positions_table.setItem(row, 0, QTableWidgetItem(self.input_symbol.text().strip()))
        self.positions_table.setItem(row, 1, QTableWidgetItem(self.input_quantity.text().strip()))
        self.positions_table.setItem(row, 2, QTableWidgetItem(price))

    def validate(self) -> bool:
        """
        Should validate that there all entries are appropriate upon pressing buy or sell button.

        :return: bool True if entries valid else False if entries not valid.

        """

        symbol = self.input_symbol.text().strip()
        qty = self.input_quantity.text()

        if not symbol:
            QMessageBox.critical(self, 'Error', 'Symbol box is blank. Please enter a symbol')
            if not symbol.isalpha():
                QMessageBox.critical(self, 'Error', "-- {symbol} -- Is Not a Valid Symbol.")

                self.clear()
                return False
            return False
        if not qty:
            QMessageBox.critical(self, 'Error', "Quantity is blank")
            if not qty.isdigit():
                QMessageBox.critical(self, 'Error', "Please Enter Valid Numerical Quantity")
                self.clear()
                return False
            return False
        match = self.symbol_match(symbol)

        if len(symbol) == 0 or match == False:
            QMessageBox.critical(self, 'Error', 'Symbol does not exist')
            return False

        return True

    def sell(self) -> None:
        """
        Should sell items from the table.
        **Function still in pregress
        :return: None
        """
        if not self.validate():
            return False

    def clear(self) -> None:
        """
        Just clears the input boxes
        :return:
        """
        self.input_symbol.clear()
        self.input_quantity.clear()

    def init_table(self) -> None:
        """
        Initates table with row one being dashes which i had thought would solve my problem.
        :return: No Return
        """
        initiate_table = [
            {'Symbol': '--', 'Quantity': '--', 'Price': '--'}
        ]
        self.positions_table.setHorizontalHeaderLabels(initiate_table[0].keys())
        self.positions_table.setRowCount(len(initiate_table))
        row = 0
        for i in initiate_table:
            self.positions_table.setItem(row, 0, QTableWidgetItem(i['Symbol']))
            self.positions_table.setItem(row, 1, QTableWidgetItem(i['Quantity']))
            self.positions_table.setItem(row, 2, QTableWidgetItem(str(i['Price'])))
            row += 1

    def get_data(self) -> str:
        """
        Pulls Data from Polygon.io & saves the price to return it by itself as
        :return: str-- value for key 'c' which in API represents previous day closing price. Actual value is a
        float but the QTableWidgetItem() functions seems to only accept Strings.
        """
        api = Logic.API
        symbol = self.symbol
        api_url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/prev?adjusted=true&apiKey={api}"

        data = requests.get(api_url).json()
        results = data['results']  # At this point the values are in a dictionary.
        info = results[0]
        price = info.get('c')
        return str(price)

    def symbol_match(self, symbol: object) -> bool:
        """
        Simply pulls data from Polygon.io API to see if the Symbol enteres exists. The database doens't have built
        in function to determine if it exists --- when I call it just gives an empty object/list of sort. So if the
        returned object is empty that is taken as indication as symbol not existing.
        :param symbol: string entered by user that is then passed directly into this function.
        :return: True if matches, False if no match.
        """
        api = Logic.API
        self.symbol = symbol
        self.api_url_ticker = f"https://api.polygon.io/v3/reference/tickers?ticker={self.symbol}&market=stocks&active=true&limit=100&apiKey={api}"
        self.data = requests.get(self.api_url_ticker).json()
        results = self.data['results']
        if len(results) == 0:
            return False
        return True
