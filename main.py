import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit
from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL.ImageQt import ImageQt

from api_utils import *
from map_show import *


class myMap:
    def __init__(self):
        self.z = 11
        self.lat = 37.619585
        self.lon = 55.865172
        self.type = 'map'
        self.toponym = 'Москва, Пестеля, 8г'
        self.spn = get_ll_spn(self.toponym)[1]
        self.count = 0
        self.pt = True


my_map = myMap()


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(550, 600))  # Устанавливаем размеры
        self.setWindowTitle("Большая задача")  # Устанавливаем заголовок окна
        self.central_widget = QWidget(self)  # Создаём центральный виджет
        self.setCentralWidget(self.central_widget)  # Устанавливаем центральный виджет
        self.grid_layout = QGridLayout()  # Создаём QGridLayout
        self.central_widget.setLayout(self.grid_layout)  # Устанавливаем данное размещение в центральный виджет
        # метка и кнопки
        self.label = QLabel()
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setText("Поиск:")
        self.grid_layout.addWidget(self.label, 0, 0, 1, 2)  # Добавляем метку в сетку
        # карта
        self.image = QLabel()
        self.grid_layout.addWidget(self.image, 1, 3, 10, 10)
        self.pixmap = QPixmap()
        self.image.setPixmap(self.pixmap)

        self.plus = QPushButton("+", self)
        self.grid_layout.addWidget(self.plus, 1, 14, 1, 1)
        self.plus.clicked.connect(self.plus_z)
        self.minus = QPushButton("-", self)
        self.grid_layout.addWidget(self.minus, 1, 0, 1, 1)
        self.minus.clicked.connect(self.minus_z)

        self.left = QPushButton("🠔", self)
        self.grid_layout.addWidget(self.left, 2, 0, 1, 1)
        self.left.clicked.connect(self.left_z)
        self.right = QPushButton("🠖", self)
        self.grid_layout.addWidget(self.right, 2, 14, 1, 1)
        self.right.clicked.connect(self.right_z)

        self.up = QPushButton("🠕", self)
        self.grid_layout.addWidget(self.up, 3, 0, 1, 1)
        self.up.clicked.connect(self.up_z)
        self.down = QPushButton("🠗", self)
        self.grid_layout.addWidget(self.down, 3, 14, 1, 1)
        self.down.clicked.connect(self.down_z)

        self.chang = QPushButton("Изменить вид карты", self)
        self.grid_layout.addWidget(self.chang, 1, 3, 1, 1)
        self.chang.clicked.connect(self.change)

        self.pochta = QPushButton("Показать почтовый индекс", self)
        self.grid_layout.addWidget(self.pochta, 1, 3, 1, 1)
        self.pochta.clicked.connect(self.mail)
        self.count_postal = 0

        self.delete = QPushButton("Сброс поискового результата", self)
        self.grid_layout.addWidget(self.delete, 1, 4, 1, 1)
        self.delete.clicked.connect(self.delete_search)

        self.adr = QLabel()
        self.grid_layout.addWidget(self.adr, 1, 5, 1, 1)
        self.adr.setText(my_map.toponym)
        # поле
        self.adress = QLineEdit()
        self.adress.setFont(font)
        self.grid_layout.addWidget(self.adress, 0, 3, 1, 10)  # Добавляем поле в сетку
        self.adress.setText(my_map.toponym)
        # поле для вывода изображения карты
        # кнопка Найти
        self.btn2 = QPushButton("Найти", self)
        self.grid_layout.addWidget(self.btn2, 0, 14, 1, 2)  # Добавляем кнопку в сетку
        self.btn2.clicked.connect(self.new_search)
        self.new_search()

    def mail(self):
        self.count_postal += 1
        p = geocode(self.adress.text())['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
        text = self.adress.text()
        if self.count_postal == 1:
            self.adr.setText(f'{text} {p}')
            self.pochta.setText("Убрать почтовый индекс")
        elif self.count_postal == 2:
            self.adr.setText(f'{text}')
            self.pochta.setText("Показать почтовый индекс")
            self.count_postal = 0

    def delete_search(self):
        my_map.pt = False
        self.new_search()

    def change(self):
        my_map.count += 1
        if my_map.count == 1:
            my_map.type = 'sat'
            self.change_map()
        elif my_map.count == 2:
            my_map.type = 'sat,skl'
            self.change_map()
        elif my_map.count == 3:
            my_map.type = 'map'
            self.change_map()
            my_map.count = 0

    def up_z(self):
        my_map.lat += 1 / my_map.lon
        self.change_map()

    def down_z(self):
        my_map.lat -= 1 / my_map.lon
        self.change_map()

    def plus_z(self):
        if my_map.z < 27:
            my_map.z += 1
        self.change_map()

    def minus_z(self):
        if my_map.z > 3:
            my_map.z -= 1
        self.change_map()

    #def KeyPressEvent(self, event):
        #if event.key() == Qt.Key_W:
            #self.plus_z()
        #elif event.key() == Qt.Key_S:
            #self.minus_z()
        #elif event.key() == Qt.Key_A:
            #self.left_z()
        #elif event.key() == Qt.Key_A:
            #self.right_z()

    def left_z(self):
        my_map.lon -= 1/my_map.lat
        self.change_map()

    def right_z(self):
        my_map.lon += 1/my_map.lat
        self.change_map()

    def new_search(self):
        if my_map.pt:
            my_map.toponym = self.adress.text()
            my_map.lon, my_map.lat = get_coords(my_map.toponym)
            self.change_map()
        else:
            self.adress.setText('')
            my_map.toponym = self.adress.text()
            self.adr.setText(my_map.toponym)
            self.change_map()

    def change_map(self):
        if my_map.pt:
            params = {
                "ll": ','.join([str(my_map.lon), str(my_map.lat)]),
                "z": str(my_map.z),
                "l": my_map.type,
                'pt': f"{my_map.lon},{my_map.lat},pm2dbm"
                }
        else:
            params = {
                "ll": ','.join([str(my_map.lon), str(my_map.lat)]),
                "z": str(my_map.z),
                "l": my_map.type
            }

        self.pixmap = QPixmap(get_map(params))
        self.image.setPixmap(self.pixmap)


app = QApplication(sys.argv)
mw = MainWindow()
mw.show()
sys.exit(app.exec())
