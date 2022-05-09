import requests
import sys

from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QTextEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QVBoxLayout

__version__ = '0.1'
__author__ = 'Ehsan shavandi'


class Window(QMainWindow):
    """Main Window."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle('Bitcoin Price')
        self._createLayout()
        self._createMenu()
        # self._createToolBar()
        self._createStatusBar()

    def _createLayout(self):
        self.generalLayout = QVBoxLayout()
        self.priceText = QTextEdit()
        self.priceText.setReadOnly(True)
        self.btn = QPushButton('Get Price')
        self.btnClear = QPushButton('Clear')
        self.btnClear.clicked.connect(self._btnClearClicked)
        self.btn.clicked.connect(self._btnClicked)
        self.generalLayout.addWidget(self.priceText)
        self.generalLayout.addWidget(self.btn)
        self.generalLayout.addWidget(self.btnClear)
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)

    def _createToolBar(self):
        tools = QToolBar()
        self.addToolBar(tools)
        tools.addAction('Exit', self.close)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("")
        self.setStatusBar(status)

    #  slots
    def _btnClicked(self):
        response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
        result = response.json()
        bitcoinPriceInDollar = result['bpi']['USD']
        bitcoinPriceInPound = result['bpi']['GBP']
        bitcoinPriceInEuro = result['bpi']['EUR']

        text = "Bitcoin Price In Dollar: "
        text += str(bitcoinPriceInDollar['rate'])
        text += "$"
        text += "\n"

        text += "Bitcoin Price In Pound: "
        text += str(bitcoinPriceInPound['rate'])
        text += "£"
        text += "\n"

        text += "Bitcoin Price In Euro: "
        text += str(bitcoinPriceInEuro['rate'])
        text += "€"
        text += "\n"

        # time
        timeUTC = result['time']['updated']
        text += str(timeUTC)

        self.priceText.setPlainText(text)

    def _btnClearClicked(self):
        self.priceText.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
