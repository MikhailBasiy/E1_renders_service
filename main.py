from PyQt6.QtCore import Qt, QSize, QUrl
from PyQt6.QtWidgets import QApplication, QCheckBox, QComboBox, QFileDialog, \
                            QLabel, QLineEdit, QListWidget, QMainWindow, \
                            QPushButton, QStatusBar, QVBoxLayout, QWidget
from PyQt6.QtGui import QIcon

from pathlib import Path

from product_properties import series, types, caseColors, profileColors
from imgs_settings import acceptable_exts
import std_naming

from icecream import ic

import logging
from datetime import datetime

logging.basicConfig(
    level="DEBUG", 
    filename=f"logs/card_conf_{datetime.now().strftime('%m-%d_%H-%M')}.log", 
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s",
    encoding='utf-8')


def _getImgsPathsList(urls: list[QUrl]) -> list[Path]:
    paths: set[str] = set()
    for url in urls:
        path = Path(url.toLocalFile())
        if path.is_dir():
            for object in path.rglob("*"):
                if object.is_file() and object.suffix in acceptable_exts:
                    ic(object)
                    paths.add(object)
        elif path.suffix in acceptable_exts:
            ic(path)
            paths.add(path)
    return paths


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
        self.imgsList: list[Path] = []

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
            
            itemsToAppend = _getImgsPathsList(event.mimeData().urls())
            self.imgsList.extend(itemsToAppend)
        else:
            event.ignore()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(QSize(700,400))
        self.setWindowIcon(QIcon("__img__/e1.png"))
        self.setWindowTitle(
            "Программа подготовки рендеров перед загрузкой на сайт Е1"
        )
        ### Выбор папки с изображениями
        self.dragNDropWidget = DragNDropWidget()

        ### Чекбоксы переименования
        self.correctNamesRequiredCBx = QCheckBox(
            "Провести проверку и исправить имена рендеров на стандартные"
        )
        self.correctNamesRequiredCBx.setChecked(True)
        self.correctNamesRequiredCBx.stateChanged.connect(self.correctNamesRequiredCBxStateChanged)
        self.renameWithIdRequiredCBx = QCheckBox(
            "Заменить названия рендеров на внешние коды соответствующих ТП"
        )
        self.renameWithIdRequiredCBx.setChecked(True)
        ### Выбор отсутствующих в названиях файлов свойств
        self.seriesCBx = EditableComboBox(
            items=series, 
            placeholder="укажите СЕРИЮ продукции"
        )
        self.wardrobeTypeCBx = EditableComboBox(
            items=types, 
            placeholder="укажите ТИП продукции"
        )
        self.caseColorCBx = EditableComboBox(
            items=caseColors,
            placeholder="укажите ЦВЕТ КОРПУСА"
        )
        self.profileColorCBx = EditableComboBox(
            items=profileColors,
            placeholder="укажите ЦВЕТ ПРОФИЛЯ"
        )
        self.frontTypeLn = QLineEdit()
        self.frontTypeLn.setPlaceholderText("укажите ТИП ФАСАДА")
        ### Кнопка запуска
        self.launchBtn = QPushButton("Запуск")
        self.launchBtn.clicked.connect(self.process_files)
        ### Служебные сообщения
        self.status = QStatusBar()
             
        layout = QVBoxLayout()
        layout.addWidget(self.dragNDropWidget)
        layout.addWidget(self.correctNamesRequiredCBx)
        layout.addWidget(self.seriesCBx)
        layout.addWidget(self.wardrobeTypeCBx)
        layout.addWidget(self.caseColorCBx)
        layout.addWidget(self.profileColorCBx)
        layout.addWidget(self.frontTypeLn)
        layout.addWidget(self.renameWithIdRequiredCBx)
        layout.addWidget(self.launchBtn)
        layout.addWidget(self.status)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def correctNamesRequiredCBxStateChanged(self, state):
        if state:
            self.seriesCBx.setEnabled(True)
            self.wardrobeTypeCBx.setEnabled(True)
            self.caseColorCBx.setEnabled(True)
            self.profileColorCBx.setEnabled(True)
            self.frontTypeLn.setEnabled(True)
        else:
            self.seriesCBx.setEnabled(False)
            self.wardrobeTypeCBx.setEnabled(False)
            self.caseColorCBx.setEnabled(False)
            self.profileColorCBx.setEnabled(False)
            self.frontTypeLn.setEnabled(False)

    def process_files(self):
        if not self.dragNDropWidget.imgsList:
            self.status.showMessage(
                "Не выбрано ни одного изображения требуемого формата",
                4000
            )
        else:
            imgsList = self.dragNDropWidget.imgsList
            ic(imgsList)
            if self.correctNamesRequiredCBx.isChecked():
                series = self.seriesCBx.currentText()
                wardrobeType = self.wardrobeTypeCBx.currentText()
                caseColor = self.caseColorCBx.currentText()
                profileColor = self.profileColorCBx.currentText()
                frontType = self.frontTypeLn.text()

                if std_naming.rename(
                    series,
                    wardrobeType,
                    caseColor,
                    profileColor,
                    frontType,
                    imgsList
                ):
                    self.status.showMessage(
                        "Файлы успешно обработаны",
                        4000
                    )
                    

        if self.renameWithIdRequiredCBx.isChecked():
            pass  
        

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()