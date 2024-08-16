import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QTableView,
                             QHBoxLayout, QVBoxLayout)
from PyQt6.QtCore import Qt

"""
class TableWidget(QTableView):
    def __init__(self, rows, columns, parent=None):
        super().__init__(rows, columns)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_V and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            selection = self.selectedIndexes()

            if selection:
                row_anchor = selection[0].row()
                column_anchor = selection[0].column()

                clipboard = QApplication.clipboard()

                rows = clipboard.text().split('\n')
                for indx_row, row in enumerate(rows):
                    values = row.split('\t')
                    for indx_col, value in enumerate(values):
                        item = QTableViewItem(value)
                        self.setItem(row_anchor + indx_row, column_anchor + indx_col, item)
            super().keyPressEvent(event)
"""

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 700, 500
        self.setMinimumSize(self.window_width, self.window_height)
        self.setStyleSheet('''
            QWidget {
                font-size: 12px;
            }
        ''')

        self.layout = {}
        self.layout['main'] = QVBoxLayout()
        self.setLayout(self.layout['main'])
        self.table = QTableView()
        self.layout['main'].addWidget(self.table)
        self.table.setHorizontalHeader('Symbol')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 17px;
        }
    ''')

    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')