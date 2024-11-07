from PyQt6.QtCore import Qt, QSize, QUrl
from PyQt6.QtWidgets import QApplication, QCheckBox, QComboBox, QFileDialog, QLabel, QListWidget, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QIcon

from product_properties import series, caseColors, types

from icecream import ic


class EditableComboBox(QComboBox):
    def __init__(self, items: list, placeholder: str):
        super().__init__()
        self.addItems(items)
        self.setEditable(True)
        self.lineEdit().setPlaceholderText("ОПЦИОНАЛЬНО: " + placeholder)


class DragNDropWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        # self.resize(QSize(300, 300))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()

            print(event.mimeData().urls())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        checkNamesRequired: bool = False
        idRenameRequired: bool = False

        self.setMinimumSize(QSize(700,400))
        self.setWindowIcon(QIcon("__img__/e1.png"))
        self.setWindowTitle(
            "Программа подготовки рендеров перед загрузкой на сайт Е1"
        )

        ### Выбор папки с изображениями

        dragNDropWidget = DragNDropWidget()

        ### Чекбокс проверки и изменения имени рендера на стандартное
        checkNamesRequiredChBx = QCheckBox(
            "Провести проверку и исправить имена рендеров на стандартные"
        )
        # checkNamesRequiredChBx.setCheckable(True)
        ### Выбор серии
        seriesCBx = EditableComboBox(
            items=series, 
            placeholder="Выберите или введите название СЕРИИ продукции"
        )
        seriesCBx.currentTextChanged.connect(self.seriesCBxTextChanged)
        ### Выбор цвета корпуса
        caseColorCBx = EditableComboBox(
            items=caseColors,
            placeholder="Выберите или введите название ЦВЕТА КОРПУСА"
        )
        caseColorCBx.currentTextChanged.connect(self.caseColorCBxTextChanged)
        ### Выбор типа продукции
        typeCBx = EditableComboBox(
            items=types, 
            placeholder="Выберите или введите ТИП продукции"
        )
        typeCBx.currentTextChanged.connect(self.typeCBxTextChanged)
        ### Чекбокс замены названий рендеров на id ТП
        idRenameRequired = QCheckBox(
            "Заменить названия рендеров на внешние коды соответствующих ТП"
        )
        ### Кнопка запуска
        launch_btn = QPushButton("Запуск")
        launch_btn.clicked.connect(lambda: self.process_files(
                checkNamesRequired,
                idRenameRequired
            )
        )
             
        layout = QVBoxLayout()
        layout.addWidget(dragNDropWidget)
        layout.addWidget(checkNamesRequiredChBx)
        layout.addWidget(seriesCBx)
        layout.addWidget(caseColorCBx)
        layout.addWidget(typeCBx)
        layout.addWidget(idRenameRequired)
        layout.addWidget(launch_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def seriesCBxTextChanged(self, series):
        print(series)

    def caseColorCBxTextChanged(self, caseColor):
        print(caseColor)

    def typeCBxTextChanged(self, type):
        print(type)

    def process_files(self, checkNamesRequired, idRenameRequired):
        if checkNamesRequired:
            print(checkNamesRequired)
        

    
        

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()