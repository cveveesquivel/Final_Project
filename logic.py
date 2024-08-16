from PyQt6.QtWidgets import *

import api
from gui import *


class Logic(QMainWindow, Ui_Dashboard):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.buy_pushButton.clicked.connect(lambda: self.buy())
        self.sell_pushButton.clicked.connect(lambda: self.sell())

    def buy(self):
        symbol = str(self.input_symbol.text()).upper()
        qty = int(self.input_quantity.text())
        price = None
        if self.validate == True:
            price = api.Polygon.get_data(symbol)

    def validate(self):
        self.symbol = self.input_symbol
        match = api.Polygon.symbol_match(self.symbol)
        if len(self.symbol) == 0 or match == False:
            return False
        return True

    def table(self):
        pass

    def sell(self):
        pass

    def clear(self):
        pass
