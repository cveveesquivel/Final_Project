import csv
from PyQt6 import QtCore, QtGui, QtWidgets
from polygon import RESTClient
import requests

import logic


class Polygon:
    """
    For purposes of this project this class is simply being used to hide the API key.
    """
    API = "EmMATDGzKUU0Lq96vumklRHczv17FHBb"

    def __init__(self, symbol, qty):
        api = Polygon.API
        self.client = RESTClient(api_key="EmMATDGzKUU0Lq96vumklRHczv17FHBb")
        self.symbol = str(self.symbol)
        self.qty = qty
        self.api_url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/prev?adjusted=true&apiKey={api}'
        Polygon.API = self.api_url

    def get_data(self):
        """

        :return: dictionary with stock info results
        """
        self.data = requests.get(self.api_url).json()
        results = self.data['results']  # At this point the values are in a dictionary.
        info = results[0]
        self.write_to_file(info)
        return results

    def symbol_match(self, *args, **kwargs):
        api = Polygon.API
        symbol = self.symbol
        self.api_url_ticker = f"https://api.polygon.io/v3/reference/tickers?ticker={symbol}&market=stocks&active=true&limit=100&apiKey={api}"
        self.data = requests.get(self.api_url_ticker).json()
        results = self.data['results']
        if len(results) == 0:
            return False
        return True

    def write_to_file(self, info):
        symbol = self.symbol
        prev_close = self.info.get('C')
        qty = self.qty

        with open('positions.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([symbol, qty, f'${prev_close}'])
