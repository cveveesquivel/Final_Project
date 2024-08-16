import csv
from PyQt6 import QtCore, QtGui, QtWidgets
from polygon import RESTClient
import requests
class Polygon:

    API = "EmMATDGzKUU0Lq96vumklRHczv17FHBb"

    def __init__(self, symbol):
        api = Polygon.API
        self.client = RESTClient(api_key="EmMATDGzKUU0Lq96vumklRHczv17FHBb")
        self.symbol = symbol
        self.api_url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/prev?adjusted=true&apiKey={api}'

    def get_data(self):
        """

        :return: dictionary with stock info results
        """
        self.data = requests.get(self.api_url).json()
        results = self.data['results'] # At this point the values are in a dictionary.
        return results
    def symbol_match(self) -> bool:
        api = Polygon.API
        self.symbol = self.symbol
        self.api_url_ticker = f"https://api.polygon.io/v3/reference/tickers?ticker={self.symbol}&market=stocks&active=true&limit=100&apiKey={api}"
        self.data = requests.get(self.api_url_ticker).json()
        results = self.data['results']
        if len(results) == 0:
            return False
        return True


    def get_price(self):
        pass