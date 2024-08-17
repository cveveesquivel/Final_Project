from PyQt6.QtWidgets import *
import csv

from gui import *
from polygon import RESTClient
import requests


class Logic(QMainWindow, Ui_Dashboard):
    API = "EmMATDGzKUU0Lq96vumklRHczv17FHBb"

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.buy_pushButton.clicked.connect(lambda: self.buy())
        self.sell_pushButton.clicked.connect(lambda: self.sell())
        self.clear_entries_pushButton.clicked.connect(lambda: self.clear())
        # api = Polygon.API
        self.client = RESTClient(api_key="EmMATDGzKUU0Lq96vumklRHczv17FHBb")
        # self.symbol = self.symbol
        # self.qty = qty
        # self.api_url = f'https://api.polygon.io/v2/aggs/ticker/{self.symbol}/prev?adjusted=true&apiKey={api}'
        # Polygon.API = self.api_url
        self.init_table()

    def buy(self):
        """

        :return: None. This method should perform validation at beginning & if succesfull
        it should add the update the Table on the GUI with the Symbol, Quantity, & Price info (pulled from API).

        """
        if not self.validate():
            return
        symbol = self.input_symbol.text().strip().upper()
        qty = self.input_quantity.text()

        price = self.get_data()
        QMessageBox.critical(self, "Notice", f'Price is {price}', )

        row = self.positions_table.rowCount()
        self.positions_table.insertRow(row)
        self.positions_table.setItem(row, 0, QTableWidgetItem(self.input_symbol.text().strip()))
        self.positions_table.setItem(row, 1, QTableWidgetItem(self.input_quantity.text().strip()))
        self.positions_table.setItem(row, 2, price)
        self.clear()

    def validate(self):
        """
        Should validate that there all entries are appropriate upon pressing buy or sell button.

        :return: bool True if entries valid else False if entries not valid.

        """
        # QMessageBox.critical(self, 'Notice', 'Entering Validation Method')
        symbol = self.input_symbol.text().strip()
        qty = self.input_quantity.text()

        if not symbol:
            QMessageBox.critical(self, 'Error', 'Symbol box is blank. Please enter a symbol')
            if not symbol.isalpha():
                QMessageBox.critical(self, 'Error', "-- {symbol} -- Is Not a Valid Symbol.")
                self.symbol.setFocus()
                return False
            return False
        if not qty:
            QMessageBox.critical(self, 'Error', "Quantity is blank")
            if not qty.isdigit():
                QMessageBox.critical(self, 'Error', "Please Enter Valid Numerical Quantity")
                self.qty.setFocus()
                return False
            return False
        match = self.symbol_match(symbol)
        # symbol = self.input_symbol
        # qty = self.input_quantity
        if len(symbol) == 0 or match == False:
            QMessageBox.critical(self, 'Error', 'Symbol does not exist')
            return False
        self.clear()

    def sell(self):
        """
        Should sell items from the table.
        **Function still in pregress
        :return: None
        """
        if not self.validate():
            return False

    def clear(self):
        """
        Just clears the input boxes
        :return:
        """
        self.input_symbol.clear()
        self.input_quantity.clear()

    def init_table(self):
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

    def get_data(self):
        """
        Pulls Data from Polygon.io & saves the price to return it by itself as
        :return: str-- value for key 'c' which in API represents previous day closing price.
        """
        QMessageBox.critical(self, "Notice", f"Entering 'get_data' method. ", )
        api = Logic.API
        symbol = self.symbol
        api_url = f"https://api.polygon.io/v3/reference/tickers?ticker={symbol}&market=stocks&active=true&limit=100&apiKey={api}"

        data = requests.get(api_url).json()
        results = data['results']  # At this point the values are in a dictionary.
        info = results[0]
        price = info.get('c')
        # self.write_to_file(info)
        QMessageBox.critical(self, "Notice", f'Price is {price}')
        return price

    def symbol_match(self, symbol):
        """
        Simply pulls data from Polygon.io API to see if the Symbol enteres exists. The database doens't have built
        in function to determine if it exists --- when I call it just gives an empty object/list of sort. So if the
        returned object is empty that is taken as indication as symbol not existing.
        :param symbol: str
        :return:
        """
        api = Logic.API
        self.symbol = symbol
        self.api_url_ticker = f"https://api.polygon.io/v3/reference/tickers?ticker={self.symbol}&market=stocks&active=true&limit=100&apiKey={api}"
        self.data = requests.get(self.api_url_ticker).json()
        results = self.data['results']
        if len(results) == 0:
            return False
        return True
