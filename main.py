from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QComboBox, QLabel, QMainWindow, QVBoxLayout, QWidget

from product_properties import series, caseColors, types

from icecream import ic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(QSize(700,400))
        self.setWindowTitle(
            "Программа подготовки рендеров перед загрузкой на сайт Е1"
        )

        ### Выбор серии
        self.seriesLbl = QLabel("Выберите серию продукции")
        self.seriesCBx = QComboBox()
        self.seriesCBx.addItems(series)
        self.seriesCBx.currentTextChanged.connect(self.seriesCBxTextChanged)
        ### Выбор цвета корпуса
        self.caseColorLbl = QLabel("Выберите цвет корпуса")
        self.caseColorCBx = QComboBox()
        self.caseColorCBx.addItems(caseColors)
        self.caseColorCBx.currentTextChanged.connect(self.caseColorCBxTextChanged)
        ### Выбор типа продукции
        self.typeLbl = QLabel("Выберите тип продукции")
        self.typeCBx = QComboBox()
        self.typeCBx.addItems(types)
        self.typeCBx.currentTextChanged.connect(self.typeCBxTextChanged)
             

        layout = QVBoxLayout()
        layout.addWidget(self.seriesLbl)
        layout.addWidget(self.seriesCBx)
        layout.addWidget(self.caseColorLbl)
        layout.addWidget(self.caseColorCBx)
        layout.addWidget(self.typeLbl)
        layout.addWidget(self.typeCBx)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def seriesCBxTextChanged(self, series):
        print(series)

    def caseColorCBxTextChanged(self, caseColor):
        print(caseColor)

    def typeCBxTextChanged(self, type):
        print(type)

        

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()