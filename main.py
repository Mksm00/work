import sys
import sqlite3

from design import Ui_MainWindow
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Browser(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.connection = sqlite3.connect("base111.db")
        self.setupUi(self)
        self.SeekBtn.clicked.connect(self.seek)
        self.second_window = None
        self.res = self.connection.cursor().execute('''SELECT name, year, genre, about, developer FROM Games 
        ''').fetchall()
        self.fill(self.res)

    def seek(self):
        if self.GameInput.text() == '':
            Game_input = 'like' + ' ' + '"' + '%' + '"'
        else:
            Game_input = '=' + ' ' + '"' + self.GameInput.text() + '"'
        if self.YearInput.text().isdigit():
            Year_input = '=' + ' ' + self.YearInput.text()
        else:
            Year_input = '>' + ' ' + '1'
        if self.GenreInput.text() == '':
            Genre_input = 'like' + ' ' + '"' + '%' + '"'
        else:
            Genre_input = '=' + ' ' + '"' + self.GenreInput.text() + '"'
        if self.DeveloperInput.text() == '':
            Developer_input = 'like' + ' ' + '"' + '%' + '"'
        else:
            Developer_input = '=' + ' ' + '"' + self.DeveloperInput.text() + '"'
        self.res = self.connection.cursor().execute('''SELECT name, year, genre, about, developer FROM Games
                                            WHERE name {} and year {} and genre {} and developer {}
                                            '''.format(Game_input, Year_input, Genre_input, Developer_input)).fetchall()
        print(self.res)
        self.fill(self.res)

    def createCellWidget(self, text, btn):
        layout = QGridLayout()
        frame = QFrame()
        frame.setLayout(layout)
        layout.addWidget(QLabel(text), 0, 0)
        btn = QPushButton(btn)
        btn.clicked.connect(self.open_secondwindow)
        layout.addWidget(btn, 1, 0)
        return frame

    def fill(self, res):
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setColumnWidth(0, 120)
        self.tableWidget.setColumnWidth(1, 50)
        self.tableWidget.setColumnWidth(2, 90)
        self.tableWidget.setColumnWidth(3, 230)
        self.tableWidget.setColumnWidth(4, 120)
        self.tableWidget.setColumnWidth(5, 300)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(self.res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            self.tableWidget.setRowHeight(i, 120)
            print(i, row)
            for j, elem in enumerate(row):
                print(j, elem)
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
            widget = self.createCellWidget('Подробнее:', row[j - 4])
            self.tableWidget.setCellWidget(
                i, 5, widget)

    def open_secondwindow(self):
        wtgame = self.sender().text()
        self.second_window = MsgBox(wtgame, self)
        self.second_window.show()


class MsgBox(QWidget):
    def __init__(self, wtgame, parent=None):
        super().__init__()
        self.connection = sqlite3.connect("base111.db")
        self.wtgame = wtgame
        self.setWindowTitle(self.wtgame)
        self.setFixedSize(900, 900)
        self.move(100, 100)
        self.pixmap = QPixmap('C:/Users/makss/PycharmProjects/pythonProject/photos/{}.jpg'.format(self.wtgame))
        print('C:/Users/makss/PycharmProjects/pythonProject/photos/{}.jpg'.format(self.wtgame))
        self.image = QLabel(self)
        self.image.setScaledContents(True)
        self.image.move(30, 100)
        self.image.resize(300, 400)
        self.image.setPixmap(self.pixmap)
        GameInfo = self.connection.cursor().execute('''SELECT * FROM Games 
                                          WHERE name = "{}" '''.format(self.wtgame)).fetchall()
        print(GameInfo)
        self.GameName = QLabel(GameInfo[0][1], self)
        self.GameName.setAlignment(Qt.AlignCenter)
        self.GameName.setFont(QFont('Arial', 16))
        self.GameName.resize(400, 100)
        self.GameName.move(250, 10)
        self.GameYear = QLabel('Год выпуска: {}'.format(GameInfo[0][2]), self)
        self.GameYear.resize(400, 50)
        self.GameYear.move(350, 130)
        self.GameYear.setFont(QFont('Arial', 12))
        self.GameGenre = QLabel('Жанр: {}'.format(GameInfo[0][3]), self)
        self.GameGenre.resize(400, 50)
        self.GameGenre.move(350, 160)
        self.GameGenre.setFont(QFont('Arial', 12))
        self.GameDeveloper = QLabel('Разработчик: {}'.format(GameInfo[0][5]), self)
        self.GameDeveloper.resize(400, 50)
        self.GameDeveloper.move(350, 190)
        self.GameDeveloper.setFont(QFont('Arial', 12))
        self.GameAbout = QLabel('Описание: {}'.format(GameInfo[0][4]), self)
        self.GameAbout.resize(400, 400)
        self.GameAbout.move(350, 250)
        self.GameAbout.setFont(QFont('Arial', 12))
        self.GameAbout.setWordWrap(True)
        self.GameAbout.setAlignment(Qt.AlignTop)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Browser()
    ex.show()
    sys.exit(app.exec())
