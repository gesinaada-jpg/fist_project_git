import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QGridLayout, QPushButton, QLabel, QWidget, \
    QHBoxLayout, QVBoxLayout, QTableWidgetItem, QMessageBox, QTableWidget
from PyQt6.QtGui import QPixmap, QPainter, QIcon, QColor
from PyQt6.QtCore import Qt, QSize
import arcade
import math
import random
import time
import sqlite3
from datetime import datetime

# Используем фиксированный размер окна
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000  # Увеличиваем высоту
SCREEN_TITLE = "Русские шашки"

# Константы доски
BOARD_SIZE = 8
SQUARE_SIZE = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 14  # Уменьшаем квадраты
# Доска будет внизу, оставляем место сверху для надписей
BOARD_OFFSET_X = (SCREEN_WIDTH - BOARD_SIZE * SQUARE_SIZE) // 2
BOARD_OFFSET_Y = 150  # Сдвигаем доску вниз

# Цвета
WHITE = arcade.color.WHITE
BLACK = arcade.color.BLACK
RED = arcade.color.RED
GREEN = arcade.color.GREEN
GRAY = arcade.color.GRAY
YELLOW = arcade.color.YELLOW
GOLD = arcade.color.GOLD
BLUE = arcade.color.BLUE

# Цвета дерева
WOOD_BG = (139, 90, 43)
WOOD_LIGHT = (184, 134, 87)
WOOD_DARK = (101, 67, 33)
WOOD_BEIGE = (245, 222, 179)

# Цвета шашек
WHITE_CHECKER = (255, 250, 240)
BLACK_CHECKER = (50, 50, 50)


class GameDB:
    def __init__(self):
        self.conn = sqlite3.connect('games.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game TEXT,
                winner TEXT,
                date TEXT
            )
        ''')
        self.conn.commit()

    def save_game(self, game, winner, date):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO history (game, winner, date) VALUES (?, ?, ?)',
                       (game, winner, date))
        self.conn.commit()

    def get_all_games(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM history ORDER BY id DESC')
        return cursor.fetchall()

    def clear_history(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM history')
        self.conn.commit()


# Глобальная БД
db = GameDB()


class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Главная форма")

        container = QWidget()
        layout = QGridLayout()

        container.setLayout(layout)
        self.setCentralWidget(container)

        layout.addWidget(QLabel(""), 0, 0)
        layout.addWidget(QLabel(""), 0, 1)
        layout.addWidget(QLabel(""), 0, 2)
        layout.addWidget(QLabel(""), 0, 3)
        layout.addWidget(QLabel(""), 0, 4)
        title = QLabel("Во что вы хотите сыграть?")
        title.setStyleSheet("font-size: 28px; color: white; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title, 0, 0, 1, 17)

        btn_checers = QPushButton()
        btn_checers.setIcon(QIcon("images/шашки.jpg"))
        btn_checers.setIconSize((QSize(295, 295)))
        btn_checers.setStyleSheet("""
            QPushButton {
                border: none;
                outline: none;
                background: transparent;
                margin: 0;
                padding: 0;
            }

            /* Рамка ВЕЗДЕ при наведении*/
            QPushButton:hover {
                border: 4px solid white;     /* толстая белая */
                background: rgba(255,255,255,80); /* полупрозрачный белый фон */
                padding: 2px;                /* отступ внутри рамки */
            }
        """)
        layout.addWidget(btn_checers, 5, 5)
        btn_checers.clicked.connect(self.checers)

        label_checers = QLabel("Шашки")
        label_checers.setStyleSheet("""
            color: #ffffff;           /* белый цвет текста */
            font-size: 24px;          /* размер шрифта */
            font-weight: bold;        /* жирный */
            font-family: Arial;       /* шрифт */
            padding: 10px;
        """)
        layout.addWidget(label_checers, 2, 5, 3, 5)

        btn_chess = QPushButton()
        btn_chess.setIcon(QIcon("images/шахматы.jpg"))
        btn_chess.setIconSize(QSize(295, 295))
        btn_chess.setStyleSheet("""
            QPushButton {
            border: none;
            outline: none;
            background: transparent;
            margin: 0;
            padding: 0;
            }
            QPushButton:hover {
            border: 4px solid white;
            background: rgba(255, 255, 255, 80);
            padding: 1px;
            }
        """)
        layout.addWidget(btn_chess, 5, 7)
        btn_chess.clicked.connect(self.chess)

        label_chess = QLabel("Шахматы")
        label_chess.setStyleSheet("""
            color: #ffffff;
            font-size: 24px;
            font-weight: bold;
            font-family: Arial;
            padding: 10px;        
        """)
        layout.addWidget(label_chess, 2, 7, 3, 5)

        btn_go = QPushButton()
        btn_go.setIcon(QIcon("images/Игра Го.jpg"))
        btn_go.setIconSize(QSize(295, 295))
        btn_go.setStyleSheet("""
            QPushButton {
            border: none;
            outline: none;
            background: transparent;
            margin: 0;
            padding: 0;
            }
            QPushButton:hover {
            border: 4px solid white;
            background: rgba(255, 255, 255, 0);
            padding: 2px;
            }
        """)
        layout.addWidget(btn_go, 13, 7)
        btn_go.clicked.connect(self.go)

        label_go = QLabel("Го")
        label_go.setStyleSheet("""
            color: #ffffff;
            font-size: 24px;
            font-weight: bold;
            font-family: Arial;
            padding: 10 px;
        """)
        layout.addWidget(label_go, 10, 7, 3, 5)

        btn_nard = QPushButton()
        btn_nard.setIcon(QIcon("images/нарды_игра.jpg"))
        btn_nard.setIconSize(QSize(295, 295))
        btn_nard.setStyleSheet("""
                    QPushButton {
                    border: none;
                    outline: none;
                    background: transparent;
                    margin: 0;
                    padding: 0;
                    }
                    QPushButton:hover {
                    border: 4px solid white;
                    background: rgba(255, 255, 255, 0);
                    padding: 2px;
                    }
                """)
        layout.addWidget(btn_nard, 13, 9)
        btn_nard.clicked.connect(self.nard)

        label_nard = QLabel("Нарды")
        label_nard.setStyleSheet("""
            color: #ffffff;
            font-size: 24px;
            font-weight: bold;
            font-family: Arial;
            padding: 10 px;
        """)
        layout.addWidget(label_nard, 10, 9, 3, 5)

        self.history_btn = QPushButton("История")
        layout.addWidget(self.history_btn, 0, 0, 2, 1)
        self.history_btn.clicked.connect(self.history_open)

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("images/фон_цветы2.jpg")
        pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio,
                               Qt.TransformationMode.SmoothTransformation)
        painter.drawPixmap(0, 0, pixmap)

    def checers(self):
        self.checers_form = Checers_Window()
        self.checers_form.showMaximized()
        self.close()

    def chess(self):
        self.chess_form = Chess_Window()
        self.chess_form.showMaximized()
        self.close()

    def go(self):
        self.go_form = Go_Window()
        self.go_form.showMaximized()
        self.close()

    def history_open(self):
        self.history = HistoryWindow()
        self.history.show()

    def nard(self):
        self.not_work = NotWorkingMessage()
        self.not_work.show()


class Checers_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Шашки")

        layout = QGridLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        layout.addWidget(QLabel(""), 0, 0)
        layout.addWidget(QLabel(""), 0, 1)
        layout.addWidget(QLabel(""), 0, 2)
        layout.addWidget(QLabel(""), 0, 3)
        layout.addWidget(QLabel(""), 0, 4)

        self.btn_back = QPushButton("назад")
        layout.addWidget(self.btn_back, 0, 0, 1, 1)
        self.btn_back.clicked.connect(self.back)

        self.label_checers_name = QLabel("В какие шашки вы хотите сыграть?")
        self.label_checers_name.setStyleSheet("""
                    color: #ffffff;
                    font-size: 24px;
                    font-weight: bold;
                    font-family: Arial;
                    padding: 10 px;
                """)
        layout.addWidget(self.label_checers_name, 0, 4, 1, 5)

        self.label_checersgame1 = QLabel("Русские шашки")
        # self.label_checersgame1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_checersgame1.setStyleSheet("""
                            color: #ffffff;
                            font-size: 24px;
                            font-weight: bold;
                            font-family: Arial;
                            padding: 10 px;
                        """)
        layout.addWidget(self.label_checersgame1, 1, 3, 1, 2)

        self.btn_checersgame1 = QPushButton()
        self.btn_checersgame1.setIcon(QIcon("images/шашки5.jpg"))
        self.btn_checersgame1.setIconSize(QSize(295, 295))
        self.btn_checersgame1.setStyleSheet("""
                            QPushButton {
                            border: none;
                            outline: none;
                            background: transparent;
                            margin: 0;
                            padding: 0;
                            }
                            QPushButton:hover {
                            border: 4px solid white;
                            background: rgba(255, 255, 255, 0);
                            padding: 2px;
                            }
                        """)
        layout.addWidget(self.btn_checersgame1, 2, 3)
        self.btn_checersgame1.clicked.connect(self.russian_checers)

        self.label_checersgame2 = QLabel("Англиские  шашки")
        # self.label_checersgame2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_checersgame2.setStyleSheet("""
                            color: #ffffff;
                            font-size: 24px;
                            font-weight: bold;
                            font-family: Arial;
                            padding: 10 px;
                        """)
        layout.addWidget(self.label_checersgame2, 1, 4, 1, 2)

        self.btn_checersgame2 = QPushButton()
        self.btn_checersgame2.setIcon(QIcon("images/шашки4.jpg"))
        self.btn_checersgame2.setIconSize(QSize(295, 295))
        self.btn_checersgame2.setStyleSheet("""
                            QPushButton {
                            border: none;
                            outline: none;
                            background: transparent;
                            margin: 0;
                            padding: 0;
                            }
                            QPushButton:hover {
                            border: 4px solid white;
                            background: rgba(255, 255, 255, 0);
                            padding: 2px;
                            }
                        """)
        layout.addWidget(self.btn_checersgame2, 2, 4)
        self.btn_checersgame2.clicked.connect(self.not_work)

        self.label_checersgame3 = QLabel("Турецкие шашки")
        # self.label_checersgame2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_checersgame3.setStyleSheet("""
                                    color: #ffffff;
                                    font-size: 24px;
                                    font-weight: bold;
                                    font-family: Arial;
                                    padding: 10 px;
                                """)
        layout.addWidget(self.label_checersgame3, 1, 5, 1, 2)

        self.btn_checersgame3 = QPushButton()
        self.btn_checersgame3.setIcon(QIcon("images/шашки2.jpg"))
        self.btn_checersgame3.setIconSize(QSize(295, 295))
        self.btn_checersgame3.setStyleSheet("""
                                    QPushButton {
                                    border: none;
                                    outline: none;
                                    background: transparent;
                                    margin: 0;
                                    padding: 0;
                                    }    
                                    QPushButton:hover {
                                    border: 4px solid white;
                                    background: rgba(255, 255, 255, 0);
                                    padding: 2px;
                                    }
                                """)
        layout.addWidget(self.btn_checersgame3, 2, 5)
        self.btn_checersgame3.clicked.connect(self.not_work)

        self.label_checersgame4 = QLabel("Международные шашки")
        # self.label_checersgame1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_checersgame4.setStyleSheet("""
                            color: #ffffff;
                            font-size: 24px;
                            font-weight: bold;
                            font-family: Arial;
                            padding: 10 px;
                        """)
        layout.addWidget(self.label_checersgame4, 3, 3, 1, 2)

        self.btn_checersgame4 = QPushButton()
        self.btn_checersgame4.setIcon(QIcon("images/шашки1.jpg"))
        self.btn_checersgame4.setIconSize(QSize(295, 295))
        self.btn_checersgame4.setStyleSheet("""
                            QPushButton {
                            border: none;
                            outline: none;
                            background: transparent;
                            margin: 0;
                            padding: 0;
                            }
                            QPushButton:hover {
                            border: 4px solid white;
                            background: rgba(255, 255, 255, 0);
                            padding: 2px;
                            }
                        """)
        layout.addWidget(self.btn_checersgame4, 4, 3)
        self.btn_checersgame4.clicked.connect(self.not_work)

        self.label_checersgame5 = QLabel("Итальянские  шашки")
        # self.label_checersgame2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_checersgame5.setStyleSheet("""
                            color: #ffffff;
                            font-size: 24px;
                            font-weight: bold;
                            font-family: Arial;
                            padding: 10 px;
                        """)
        layout.addWidget(self.label_checersgame5, 3, 5, 1, 2)

        self.btn_checersgame5 = QPushButton()
        self.btn_checersgame5.setIcon(QIcon("images/шашки_все.jpg"))
        self.btn_checersgame5.setIconSize(QSize(295, 295))
        self.btn_checersgame5.setStyleSheet("""
                            QPushButton {
                            border: none;
                            outline: none;
                            background: transparent;
                            margin: 0;
                            padding: 0;
                            }
                            QPushButton:hover {
                            border: 4px solid white;
                            background: rgba(255, 255, 255, 0);
                            padding: 2px;
                            }
                        """)
        layout.addWidget(self.btn_checersgame5, 4, 5)
        self.btn_checersgame5.clicked.connect(self.not_work)

        self.label_checersgame6 = QLabel("Тайские шашки")
        # self.label_checersgame2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_checersgame6.setStyleSheet("""
                                    color: #ffffff;
                                    font-size: 24px;
                                    font-weight: bold;
                                    font-family: Arial;
                                    padding: 10 px;
                                """)
        layout.addWidget(self.label_checersgame6, 3, 4, 1, 2)

        self.btn_checersgame3 = QPushButton()
        self.btn_checersgame3.setIcon(QIcon("images/шашки6.jpg"))
        self.btn_checersgame3.setIconSize(QSize(295, 295))
        self.btn_checersgame3.setStyleSheet("""
                                    QPushButton {
                                    border: none;
                                    outline: none;
                                    background: transparent;
                                    margin: 0;
                                    padding: 0;
                                    }    
                                    QPushButton:hover {
                                    border: 4px solid white;
                                    background: rgba(255, 255, 255, 0);
                                    padding: 2px;
                                    }
                                """)
        layout.addWidget(self.btn_checersgame3, 4, 4)
        self.btn_checersgame3.clicked.connect(self.not_work)

    def russian_checers(self):
        russian_window = CheckersGame()
        self.close()
        arcade.run()

    def back(self):
        self.main_form = Main_Window()
        self.main_form.showMaximized()
        self.close()

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("images/фон_шашки3.jpg")
        pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio,
                               Qt.TransformationMode.SmoothTransformation)
        painter.drawPixmap(0, 0, pixmap)

    def not_work(self):
        self.not_work = NotWorkingMessage()
        self.not_work.show()


class Chess_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Шахматы")

        layout = QGridLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        layout.addWidget(QLabel(""), 0, 1)
        layout.addWidget(QLabel(""), 1, 0)
        layout.addWidget(QLabel(""), 2, 0)
        layout.addWidget(QLabel(""), 3, 0)
        layout.addWidget(QLabel(""), 4, 0)
        layout.addWidget(QLabel(""), 5, 0)
        layout.addWidget(QLabel(""), 6, 0)

        self.btn_back = QPushButton("назад")
        layout.addWidget(self.btn_back, 0, 0, 1, 1)
        self.btn_back.clicked.connect(self.back)

        layout.addWidget(QLabel(""), 0, 7)
        self.label_name = QLabel("Шахматы")

        self.label_name.setStyleSheet("""
                            color: #ffffff;
                            font-size: 24px;
                            font-weight: bold;
                            font-family: Arial;
                            padding: 10 px;
                        """)
        layout.addWidget(self.label_name, 0, 10, 1, 6)

        self.label_chessgame = QLabel("Игра в шахматы")
        self.label_chessgame.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_chessgame.setStyleSheet("""
            color: #ffffff;
            font-size: 24px;
            font-weight: bold;
            font-family: Arial;
            padding: 10 px;
        """)
        layout.addWidget(self.label_chessgame, 2, 5)

        self.btn_chessgame = QPushButton()
        self.btn_chessgame.setIcon(QIcon("images/шахматы_игра.jpg"))
        self.btn_chessgame.setIconSize(QSize(295, 295))
        self.btn_chessgame.setStyleSheet("""
                    QPushButton {
                    border: none;
                    outline: none;
                    background: transparent;
                    margin: 0;
                    padding: 0;
                    }
                    QPushButton:hover {
                    border: 4px solid white;
                    background: rgba(255, 255, 255, 0);
                    padding: 2px;
                    }
                """)
        layout.addWidget(self.btn_chessgame, 3, 5)
        self.btn_chessgame.clicked.connect(self.open_game)

        self.label_chesslevel = QLabel("Задачки")
        self.label_chesslevel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_chesslevel.setStyleSheet("""
            color: #ffffff;
            font-size: 24px;
            font-weight: bold;
            font-family: Arial;
            padding: 10 px;
        """)
        layout.addWidget(self.label_chesslevel, 2, 13)

        self.btn_chesslevel = QPushButton()
        self.btn_chesslevel.setIcon(QIcon("images/шахматы задачи.jpg"))
        self.btn_chesslevel.setIconSize(QSize(295, 295))
        self.btn_chesslevel.setStyleSheet("""
                    QPushButton {
                    border: none;
                    outline: none;
                    background: transparent;
                    margin: 0;
                    padding: 0;
                    }
                    QPushButton:hover {
                    border: 4px solid white;
                    background: rgba(255, 255, 255, 0);
                    padding: 2px;
                    }
                """)
        layout.addWidget(self.btn_chesslevel, 3, 13)
        self.btn_chesslevel.clicked.connect(self.not_work)

    def open_game(self):
        import subprocess
        import sys
        import time

        self.hide()

        # Запускаем процесс без ожидания
        process = subprocess.Popen([sys.executable, "chess_file.py"])

        # Периодически проверяем, жив ли процесс
        while process.poll() is None:
            pass

        # Процесс завершился - показываем окно
        self.showMaximized()

    def back(self):
        self.main_form = Main_Window()
        self.main_form.showMaximized()
        self.close()

    def not_work(self):
        self.not_work = NotWorkingMessage()
        self.not_work.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("images/доска1.jpg")
        pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio,
                               Qt.TransformationMode.SmoothTransformation)
        painter.drawPixmap(0, 0, pixmap)


class Go_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Игра в Го")

        layout = QGridLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        layout.addWidget(QLabel(""), 0, 1)
        layout.addWidget(QLabel(""), 1, 0)
        layout.addWidget(QLabel(""), 2, 0)
        layout.addWidget(QLabel(""), 3, 0)
        layout.addWidget(QLabel(""), 4, 0)
        layout.addWidget(QLabel(""), 5, 0)
        layout.addWidget(QLabel(""), 6, 0)

        self.btn_back = QPushButton("назад")
        layout.addWidget(self.btn_back, 0, 0, 1, 1)
        self.btn_back.clicked.connect(self.back)

        layout.addWidget(QLabel(""), 0, 7)
        self.label_name = QLabel("Игра в Го")

        self.label_name.setStyleSheet("""
                            color: #00000;
                            font-size: 24px;
                            font-weight: bold;
                            font-family: Arial;
                            padding: 10 px;
                        """)
        layout.addWidget(self.label_name, 0, 13, 1, 6)

        self.label_gogame = QLabel("Го(японская версия)")
        self.label_gogame.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_gogame.setStyleSheet("""
            color: #00000;
            font-size: 24px;
            font-weight: bold;
            font-family: Arial;
            padding: 10 px;
        """)
        layout.addWidget(self.label_gogame, 2, 8)

        self.btn_gogame = QPushButton()
        self.btn_gogame.setIcon(QIcon("images/го_игра1.jpg"))
        self.btn_gogame.setIconSize(QSize(295, 295))
        self.btn_gogame.setStyleSheet("""
                    QPushButton {
                    border: none;
                    outline: none;
                    background: transparent;
                    margin: 0;
                    padding: 0;
                    }
                    QPushButton:hover {
                    border: 4px solid white;
                    background: rgba(255, 255, 255, 0);
                    padding: 2px;
                    }
                """)
        layout.addWidget(self.btn_gogame, 3, 8)

        self.label_golevel = QLabel("Го(китайская версия)")
        self.label_golevel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_golevel.setStyleSheet("""
            color: #00000;
            font-size: 24px;
            font-weight: bold;
            font-family: Arial;
            padding: 10 px;
        """)
        layout.addWidget(self.label_golevel, 2, 15)

        self.btn_golevel = QPushButton()
        self.btn_golevel.setIcon(QIcon("images/го_игра.jpg"))
        self.btn_golevel.setIconSize(QSize(295, 295))
        self.btn_golevel.setStyleSheet("""
                    QPushButton {
                    border: none;
                    outline: none;
                    background: transparent;
                    margin: 0;
                    padding: 0;
                    }
                    QPushButton:hover {
                    border: 4px solid white;
                    background: rgba(255, 255, 255, 0);
                    padding: 2px;
                    }
                """)
        layout.addWidget(self.btn_golevel, 3, 15)
        self.btn_gogame.clicked.connect(self.not_work)
        self.btn_golevel.clicked.connect(self.not_work)

    def back(self):
        self.main_form = Main_Window()
        self.main_form.showMaximized()
        self.close()

    def not_work(self):
        self.not_work = NotWorkingMessage()
        self.not_work.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("images/го_фон3.jpg")
        pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio,
                               Qt.TransformationMode.SmoothTransformation)
        painter.drawPixmap(0, 0, pixmap)


class Particle:
    # Класс для частиц эффектов

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(5, 15)
        self.speed_x = random.uniform(-3, 3)
        self.speed_y = random.uniform(2, 6)
        self.life = 1.0
        self.decay = random.uniform(0.02, 0.05)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.speed_y -= 0.1
        self.life -= self.decay
        self.size *= 0.98

    def draw(self):
        if self.life > 0:
            alpha = int(self.life * 255)
            color_with_alpha = (*self.color, alpha)
            arcade.draw_circle_filled(self.x, self.y, self.size, color_with_alpha)


class Confetti:
    # Класс для конфетти
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.colors = [
            (255, 50, 50),
            (50, 255, 50),
            (50, 50, 255),
            (255, 255, 50),
            (255, 50, 255),
            (50, 255, 255),
        ]
        self.color = random.choice(self.colors)
        self.size = random.randint(4, 8)
        self.speed_x = random.uniform(-4, 4)
        self.speed_y = random.uniform(3, 8)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-5, 5)
        self.life = 1.0
        self.decay = random.uniform(0.01, 0.03)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.speed_y -= 0.15
        self.rotation += self.rotation_speed
        self.life -= self.decay

    def draw(self):
        if self.life > 0:
            alpha = int(self.life * 255)
            color_with_alpha = (*self.color, alpha)
            arcade.draw_rect_filled(arcade.rect.XYWH(self.x, self.y,
                                                     self.size, self.size),
                                    color_with_alpha,
                                    tilt_angle=self.rotation)


class Checker:
    # Класс шашки

    def __init__(self, row, col, is_white, is_king=False):
        self.row = row
        self.col = col
        self.is_white = is_white
        self.is_king = is_king
        self.radius = SQUARE_SIZE // 2 - 5

    def draw(self, board_offset_x, board_offset_y, square_size):
        # Отрисовка шашки
        x = board_offset_x + self.col * square_size + square_size // 2
        y = board_offset_y + self.row * square_size + square_size // 2

        checker_color = WHITE_CHECKER if self.is_white else BLACK_CHECKER
        arcade.draw_circle_filled(x, y, self.radius, checker_color)

        outline_color = BLACK if self.is_white else WHITE
        arcade.draw_circle_outline(x, y, self.radius, outline_color, 2)

        if self.is_king:
            crown_color = YELLOW if self.is_white else (200, 200, 200)
            crown_size = self.radius // 2
            arcade.draw_rect_filled(arcade.rect.XYWH(x, y + crown_size // 2,
                                                     crown_size * 2, crown_size),
                                    crown_color)
            for i in range(3):
                crown_x = x - crown_size + i * crown_size
                arcade.draw_rect_filled(arcade.rect.XYWH(crown_x, y + crown_size,
                                                         crown_size // 2, crown_size),
                                        crown_color)

        return x, y


class GameSoundManager:
    # звуки игры

    def __init__(self):
        # Флаг, что звук победы уже проигран
        self.victory_sound_played = False

    def play_victory_sound(self):
        if not self.victory_sound_played:
            try:
                import winsound
                tones = [(523, 300), (659, 300), (784, 300), (1047, 500)]
                for i, (freq, duration) in enumerate(tones):
                    winsound.Beep(freq, duration)
                    time.sleep(0.05)  # Маленькая пауза

                self.victory_sound_played = True

            except Exception as e:
                pass

    def play_move_sound(self):
        # Короткий звук при ходе/выборе шашки
        try:
            import winsound
            winsound.Beep(400, 50)
        except:
            pass

    def play_capture_sound(self):
        # Звук при взятии шашки
        try:
            import winsound
            winsound.Beep(600, 100)
            time.sleep(0.05)
            winsound.Beep(400, 80)
        except:
            pass

    def play_king_sound(self):
        # Звук при превращении в дамку
        try:
            import winsound
            winsound.Beep(800, 150)
            time.sleep(0.1)
            winsound.Beep(1000, 200)
        except:
            pass

    def reset(self):
        # Сброс флагов звуков при новой игре
        self.victory_sound_played = False


class CheckersGame(arcade.Window):
    # Основной класс игры

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
        arcade.set_background_color(WOOD_BG)

        # Инициализируем менеджер звуков
        self.sound_manager = GameSoundManager()

        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.selected_checker = None
        self.white_count = 12
        self.black_count = 12
        self.current_player = True
        self.valid_moves = []
        self.show_rules = False

        # Переменные для анимации победы
        self.game_over = False
        self.winner = None
        self.victory_timer = 0
        self.camera_shake = 0
        self.camera_shake_intensity = 0
        self.confetti_particles = []
        self.sparkle_particles = []
        self.victory_message_alpha = 0
        self.victory_scale = 1.0
        self.show_victory_message = False

        self.move_made = False  # Был ли сделан ход
        self.capture_made = False  # Было ли взятие
        self.king_created = False  # Было ли превращение в дамку

        # Для тряски камеры
        self.shake_offset_x = 0
        self.shake_offset_y = 0
        self.move_count = 0

        self.setup_board()

    def setup_board(self):
        # Начальная расстановка шашек
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        for row in range(3):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 1:
                    self.board[row][col] = Checker(row, col, False)

        for row in range(5, BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 1:
                    self.board[row][col] = Checker(row, col, True)

        self.white_count = 12
        self.black_count = 12
        self.current_player = True
        self.selected_checker = None
        self.valid_moves = []
        self.game_over = False
        self.winner = None
        self.victory_timer = 0
        self.camera_shake = 0
        self.confetti_particles = []
        self.sparkle_particles = []
        self.victory_message_alpha = 0
        self.victory_scale = 1.0
        self.show_victory_message = False

        self.move_made = False
        self.capture_made = False
        self.king_created = False

        # Сброс звуков
        self.sound_manager.reset()

        self.shake_offset_x = 0
        self.shake_offset_y = 0
        self.move_count = 0

    def trigger_victory(self, winner):
        # Запуск анимации победы
        self.game_over = True
        date_str = datetime.now().strftime("%d.%m.%Y %H:%M")
        db.save_game("Русские шашки", winner, date_str)
        self.camera_shake = 30  # 30 кадров тряски
        self.camera_shake_intensity = 10
        self.show_victory_message = True

        # Создаем конфетти по всей доске
        board_center_x = BOARD_OFFSET_X + (BOARD_SIZE * SQUARE_SIZE) // 2
        board_center_y = BOARD_OFFSET_Y + (BOARD_SIZE * SQUARE_SIZE) // 2

        for _ in range(100):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, BOARD_SIZE * SQUARE_SIZE // 2)
            x = board_center_x + math.cos(angle) * distance
            y = board_center_y + math.sin(angle) * distance
            self.confetti_particles.append(Confetti(x, y))

        # Создаем искры вокруг шашек победителя
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                checker = self.board[row][col]
                if checker and checker.is_white == (winner == "white"):
                    x = BOARD_OFFSET_X + col * SQUARE_SIZE + SQUARE_SIZE // 2
                    y = BOARD_OFFSET_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2
                    for _ in range(20):
                        self.sparkle_particles.append(Particle(x, y,
                                                               (255, 255, 200) if winner == "white" else (50, 50, 100)))

    def update_particles(self):
        # Обновляем конфетти
        for particle in self.confetti_particles[:]:
            particle.update()
            if particle.life <= 0:
                self.confetti_particles.remove(particle)

        # Обновляем искры
        for particle in self.sparkle_particles[:]:
            particle.update()
            if particle.life <= 0:
                self.sparkle_particles.remove(particle)

        # Добавляем новые искры если игра закончена
        if self.game_over and random.random() < 0.3:
            board_center_x = BOARD_OFFSET_X + (BOARD_SIZE * SQUARE_SIZE) // 2
            board_center_y = BOARD_OFFSET_Y + (BOARD_SIZE * SQUARE_SIZE) // 2
            angle = random.uniform(0, 2 * math.pi)
            radius = random.uniform(50, 300)
            x = board_center_x + math.cos(angle) * radius
            y = board_center_y + math.sin(angle) * radius

            particle_color = (255, 255, 200) if self.winner == "white" else (50, 50, 100)
            self.sparkle_particles.append(Particle(x, y, particle_color))

    def on_draw(self):
        self.clear()

        current_width = self.width
        current_height = self.height
        square_size = min(current_width, current_height) // 14
        board_offset_x = (current_width - BOARD_SIZE * square_size) // 2
        board_offset_y = 150

        # Кнопки ПОД доской
        buttons_y = 50

        for row in self.board:
            for checker in row:
                if checker:
                    checker.radius = square_size // 2 - 5

        # Применяем тряску камеры
        if self.camera_shake > 0:
            self.shake_offset_x = random.uniform(-self.camera_shake_intensity, self.camera_shake_intensity)
            self.shake_offset_y = random.uniform(-self.camera_shake_intensity, self.camera_shake_intensity)
            self.camera_shake -= 1
            self.camera_shake_intensity *= 0.9
        else:
            self.shake_offset_x = 0
            self.shake_offset_y = 0

        # Рисуем
        self.draw_wood_texture(current_width, current_height, self.shake_offset_x, self.shake_offset_y)

        self.draw_title(current_width, current_height, self.shake_offset_x, self.shake_offset_y)

        if not self.game_over:
            self.draw_current_player_indicator(current_width, current_height, self.shake_offset_x, self.shake_offset_y)

        self.draw_back_button(current_width, current_height, self.shake_offset_x, self.shake_offset_y)

        self.draw_board_frame(board_offset_x, board_offset_y, square_size, self.shake_offset_x, self.shake_offset_y)

        self.draw_score_boards(board_offset_x, board_offset_y, square_size, current_width, self.shake_offset_x,
                               self.shake_offset_y)

        self.draw_board(board_offset_x, board_offset_y, square_size, self.shake_offset_x, self.shake_offset_y)

        self.draw_checkers(board_offset_x, board_offset_y, square_size, self.shake_offset_x, self.shake_offset_y)

        self.draw_bottom_buttons(board_offset_x, board_offset_y, square_size, current_width, buttons_y,
                                 self.shake_offset_x, self.shake_offset_y)

        for particle in self.confetti_particles:
            particle.draw()

        for particle in self.sparkle_particles:
            particle.draw()

        if self.show_victory_message:
            self.draw_victory_message(current_width, current_height)

        if self.show_rules:
            self.draw_rules(current_width, current_height, self.shake_offset_x, self.shake_offset_y)

    def draw_wood_texture(self, width, height, offset_x=0, offset_y=0):
        stripe_width = 50
        for i in range(0, width, stripe_width):
            color = WOOD_LIGHT if (i // stripe_width) % 2 == 0 else WOOD_BG
            arcade.draw_rect_filled(arcade.rect.XYWH(i + stripe_width // 2 + offset_x,
                                                     height // 2 + offset_y,
                                                     stripe_width, height),
                                    color)

    def draw_title(self, width, height, offset_x=0, offset_y=0):
        # Рисуем заголовок
        title_y = height - 60 + offset_y
        arcade.draw_rect_filled(arcade.rect.XYWH(width // 2 + offset_x, title_y,
                                                 width * 0.8, 60),
                                WOOD_DARK)
        arcade.draw_rect_outline(arcade.rect.XYWH(width // 2 + offset_x, title_y,
                                                  width * 0.8, 60),
                                 WOOD_LIGHT, 4)
        font_size = min(48, width // 30)
        arcade.draw_text("РУССКИЕ ШАШКИ", width // 2 + offset_x, title_y,
                         WHITE, font_size, anchor_x="center", anchor_y="center",
                         bold=True)

    def draw_current_player_indicator(self, width, height, offset_x=0, offset_y=0):
        indicator_width = 450
        indicator_height = 55
        indicator_x = width // 2 + offset_x
        indicator_y = height - 130 + offset_y

        player_text = "ХОД БЕЛЫХ" if self.current_player else "ХОД ЧЕРНЫХ"
        player_bg_color = WOOD_BEIGE if self.current_player else WOOD_DARK
        player_text_color = WOOD_DARK if self.current_player else WHITE

        arcade.draw_rect_filled(arcade.rect.XYWH(indicator_x, indicator_y,
                                                 indicator_width, indicator_height),
                                player_bg_color)
        arcade.draw_rect_outline(arcade.rect.XYWH(indicator_x, indicator_y,
                                                  indicator_width, indicator_height),
                                 WOOD_LIGHT, 4)

        font_size = min(30, indicator_width // 15)
        arcade.draw_text(player_text, indicator_x, indicator_y,
                         player_text_color, font_size, anchor_x="center", anchor_y="center",
                         bold=True)

    def draw_victory_message(self, width, height):
        # Рисуем сообщение о победе
        # Для пульсации
        self.victory_message_alpha = min(1.0, self.victory_message_alpha + 0.02)
        self.victory_scale = 1.0 + 0.1 * math.sin(time.time() * 3)

        # Полупрозрачный фон
        arcade.draw_rect_filled(arcade.rect.XYWH(width // 2, height // 2,
                                                 width, height),
                                (0, 0, 0, int(150 * self.victory_message_alpha)))

        # Большая рамка победы
        frame_width = 600
        frame_height = 300
        frame_x = width // 2
        frame_y = height // 2

        # Золотая рамка с пульсацией
        glow_color = (255, 215, 0, int(200 * self.victory_message_alpha))  # Золотой
        arcade.draw_rect_filled(arcade.rect.XYWH(frame_x, frame_y,
                                                 frame_width * self.victory_scale,
                                                 frame_height * self.victory_scale),
                                glow_color)

        # Внутренняя рамка
        inner_color = (139, 90, 43, int(255 * self.victory_message_alpha))  # Дерево
        arcade.draw_rect_filled(arcade.rect.XYWH(frame_x, frame_y,
                                                 frame_width - 20,
                                                 frame_height - 20),
                                inner_color)

        winner_text = "ПОБЕДА БЕЛЫХ!" if self.winner == "white" else "ПОБЕДА ЧЕРНЫХ!"
        text_color = (255, 255, 255) if self.winner == "white" else (255, 255, 200)

        arcade.draw_text(winner_text, frame_x, frame_y + 50,
                         text_color, 48 * self.victory_scale,
                         anchor_x="center", anchor_y="center",
                         bold=True)

        arcade.draw_text("ИГРА ОКОНЧЕНА", frame_x, frame_y - 30,
                         (255, 255, 255), 32,
                         anchor_x="center", anchor_y="center",
                         bold=True)

        # Кнопка "Новая игра"
        button_width = 200
        button_height = 60
        button_x = frame_x
        button_y = frame_y - 100

        glow = 0.5 + 0.5 * math.sin(time.time() * 2)
        button_glow_color = (0, 200, 0, int(100 * glow * self.victory_message_alpha))
        arcade.draw_rect_filled(arcade.rect.XYWH(button_x, button_y,
                                                 button_width + 10,
                                                 button_height + 10),
                                button_glow_color)

        arcade.draw_rect_filled(arcade.rect.XYWH(button_x, button_y,
                                                 button_width, button_height),
                                GREEN)
        arcade.draw_rect_outline(arcade.rect.XYWH(button_x, button_y,
                                                  button_width, button_height),
                                 WHITE, 3)

        arcade.draw_text("НОВАЯ ИГРА", button_x, button_y,
                         WHITE, 24, anchor_x="center", anchor_y="center",
                         bold=True)

        self.victory_button_rect = (button_x - button_width // 2, button_y - button_height // 2,
                                    button_x + button_width // 2, button_y + button_height // 2)

    def draw_back_button(self, width, height, offset_x=0, offset_y=0):
        back_button_width = 120
        back_button_height = 45
        back_button_x = 20 + back_button_width // 2 + offset_x
        back_button_y = height - 60 + offset_y

        self.back_button_rect = (back_button_x - back_button_width // 2,
                                 back_button_y - back_button_height // 2,
                                 back_button_x + back_button_width // 2,
                                 back_button_y + back_button_height // 2)

        arcade.draw_rect_filled(arcade.rect.XYWH(back_button_x, back_button_y,
                                                 back_button_width, back_button_height),
                                BLUE)
        arcade.draw_rect_outline(arcade.rect.XYWH(back_button_x, back_button_y,
                                                  back_button_width, back_button_height),
                                 WHITE, 3)
        arcade.draw_text("НАЗАД", back_button_x, back_button_y,
                         WHITE, 18, anchor_x="center", anchor_y="center",
                         bold=True)

    def draw_board_frame(self, board_offset_x, board_offset_y, square_size, offset_x=0, offset_y=0):
        frame_size = 25
        frame_x = board_offset_x - frame_size + offset_x
        frame_y = board_offset_y - frame_size + offset_y
        frame_width = BOARD_SIZE * square_size + 2 * frame_size
        frame_height = BOARD_SIZE * square_size + 2 * frame_size

        arcade.draw_rect_filled(arcade.rect.XYWH(frame_x + frame_width // 2,
                                                 frame_y + frame_height // 2,
                                                 frame_width, frame_height),
                                WOOD_DARK)
        arcade.draw_rect_outline(arcade.rect.XYWH(frame_x + frame_width // 2,
                                                  frame_y + frame_height // 2,
                                                  frame_width, frame_height),
                                 WOOD_LIGHT, 5)

    def draw_score_boards(self, board_offset_x, board_offset_y, square_size, width, offset_x=0, offset_y=0):
        score_width = min(200, width // 8)
        score_height = 80

        white_score_x = board_offset_x - score_width // 2 - 40 + offset_x
        white_score_y = board_offset_y + BOARD_SIZE * square_size // 2 + offset_y

        arcade.draw_rect_filled(arcade.rect.XYWH(white_score_x, white_score_y,
                                                 score_width, score_height),
                                WOOD_DARK)
        arcade.draw_rect_outline(arcade.rect.XYWH(white_score_x, white_score_y,
                                                  score_width, score_height),
                                 WOOD_LIGHT, 3)

        font_size = min(24, score_width // 10)
        arcade.draw_text("БЕЛЫЕ", white_score_x, white_score_y + 25,
                         WHITE_CHECKER, font_size, anchor_x="center", bold=True)
        arcade.draw_text(str(self.white_count), white_score_x, white_score_y - 15,
                         WHITE_CHECKER, font_size + 8, anchor_x="center", bold=True)

        black_score_x = board_offset_x + BOARD_SIZE * square_size + score_width // 2 + 40 + offset_x
        black_score_y = board_offset_y + BOARD_SIZE * square_size // 2 + offset_y

        arcade.draw_rect_filled(arcade.rect.XYWH(black_score_x, black_score_y,
                                                 score_width, score_height),
                                WOOD_DARK)
        arcade.draw_rect_outline(arcade.rect.XYWH(black_score_x, black_score_y,
                                                  score_width, score_height),
                                 WOOD_LIGHT, 3)

        arcade.draw_text("ЧЕРНЫЕ", black_score_x, black_score_y + 25,
                         WHITE, font_size, anchor_x="center", bold=True)
        arcade.draw_text(str(self.black_count), black_score_x, black_score_y - 15,
                         WHITE, font_size + 8, anchor_x="center", bold=True)

    def draw_bottom_buttons(self, board_offset_x, board_offset_y, square_size, width, buttons_y, offset_x=0,
                            offset_y=0):
        # Рисуем кнопки снизу
        button_width = min(300, width // 5)
        button_height = 70
        button_spacing = 100

        start_x = width // 2 - button_width - button_spacing // 2 + offset_x

        rules_x = start_x + button_width // 2
        self.rules_button_rect = (rules_x - button_width // 2, buttons_y - button_height // 2,
                                  rules_x + button_width // 2, buttons_y + button_height // 2)

        arcade.draw_rect_filled(arcade.rect.XYWH(rules_x, buttons_y + offset_y,
                                                 button_width, button_height),
                                GRAY)
        arcade.draw_rect_outline(arcade.rect.XYWH(rules_x, buttons_y + offset_y,
                                                  button_width, button_height),
                                 WHITE, 3)

        font_size = min(26, button_width // 12)
        arcade.draw_text("ПРАВИЛА ИГРЫ", rules_x, buttons_y + offset_y,
                         WHITE, font_size, anchor_x="center", anchor_y="center",
                         bold=True)

        new_game_x = start_x + button_width + button_spacing + button_width // 2
        self.new_game_button_rect = (new_game_x - button_width // 2, buttons_y - button_height // 2,
                                     new_game_x + button_width // 2, buttons_y + button_height // 2)

        arcade.draw_rect_filled(arcade.rect.XYWH(new_game_x, buttons_y + offset_y,
                                                 button_width, button_height),
                                GREEN)
        arcade.draw_rect_outline(arcade.rect.XYWH(new_game_x, buttons_y + offset_y,
                                                  button_width, button_height),
                                 WHITE, 3)
        arcade.draw_text("НОВАЯ ИГРА", new_game_x, buttons_y + offset_y,
                         WHITE, font_size, anchor_x="center", anchor_y="center",
                         bold=True)

    def draw_board(self, board_offset_x, board_offset_y, square_size, offset_x=0, offset_y=0):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x = board_offset_x + col * square_size + offset_x
                y = board_offset_y + row * square_size + offset_y

                if (row + col) % 2 == 0:
                    color = WOOD_BEIGE
                else:
                    color = WOOD_DARK

                arcade.draw_rect_filled(arcade.rect.XYWH(x + square_size // 2,
                                                         y + square_size // 2,
                                                         square_size, square_size),
                                        color)

                if self.selected_checker and (row, col) in self.valid_moves:
                    arcade.draw_rect_filled(arcade.rect.XYWH(x + square_size // 2,
                                                             y + square_size // 2,
                                                             square_size, square_size),
                                            (0, 255, 0, 150))

                arcade.draw_rect_outline(arcade.rect.XYWH(x + square_size // 2,
                                                          y + square_size // 2,
                                                          square_size, square_size),
                                         WOOD_LIGHT, 1)

    def draw_checkers(self, board_offset_x, board_offset_y, square_size, offset_x=0, offset_y=0):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                checker = self.board[row][col]
                if checker:
                    x = board_offset_x + checker.col * square_size + square_size // 2 + offset_x
                    y = board_offset_y + checker.row * square_size + square_size // 2 + offset_y

                    checker_color = WHITE_CHECKER if checker.is_white else BLACK_CHECKER
                    arcade.draw_circle_filled(x, y, checker.radius, checker_color)

                    outline_color = BLACK if checker.is_white else WHITE
                    arcade.draw_circle_outline(x, y, checker.radius, outline_color, 2)

                    if checker.is_king:
                        crown_color = YELLOW if checker.is_white else (200, 200, 200)
                        crown_size = checker.radius // 2
                        arcade.draw_rect_filled(arcade.rect.XYWH(x, y + crown_size // 2,
                                                                 crown_size * 2, crown_size),
                                                crown_color)
                        for i in range(3):
                            crown_x = x - crown_size + i * crown_size
                            arcade.draw_rect_filled(arcade.rect.XYWH(crown_x, y + crown_size,
                                                                     crown_size // 2, crown_size),
                                                    crown_color)

                    if self.selected_checker == checker:
                        arcade.draw_circle_outline(x, y, square_size // 2 - 2,
                                                   YELLOW, 4)

    def draw_rules(self, width, height, offset_x=0, offset_y=0):
        arcade.draw_rect_filled(arcade.rect.XYWH(width // 2 + offset_x, height // 2 + offset_y,
                                                 width - 200, height - 200),
                                (0, 0, 0, 220))

        arcade.draw_rect_filled(arcade.rect.XYWH(width // 2 + offset_x, height // 2 + offset_y,
                                                 width - 250, height - 250),
                                WOOD_DARK)
        arcade.draw_rect_outline(arcade.rect.XYWH(width // 2 + offset_x, height // 2 + offset_y,
                                                  width - 250, height - 250),
                                 WOOD_LIGHT, 6)

        font_size = min(36, width // 40)
        arcade.draw_text("ПРАВИЛА РУССКИХ ШАШЕК", width // 2 + offset_x, height - 150 + offset_y,
                         WHITE, font_size, anchor_x="center", bold=True)

        rules = [
            "1. Игра ведется на доске 8×8 клеток",
            "2. У каждого игрока по 12 шашек",
            "3. Шашки ходят по диагонали вперед на 1 клетку",
            "4. Для взятия нужно перепрыгнуть через шашку противника",
            "5. Шашка становится дамкой на последней горизонтали",
            "6. Дамка может ходить на любое расстояние по диагонали",
            "7. Если есть возможность бить - бить обязательно",
            "8. Можно бить несколько шашек за один ход",
            "9. Цель: съесть все шашки противника или запереть их",
            "10. Игра заканчивается, когда у одного из игроков не осталось шашек"
        ]

        y_pos = height - 220 + offset_y
        rule_font_size = min(22, width // 60)
        for rule in rules:
            arcade.draw_text(rule, width // 2 - 400 + offset_x, y_pos, WHITE, rule_font_size, width=800)
            y_pos -= 40

        close_button_width = 250
        close_button_height = 70
        close_button_x = width // 2 + offset_x
        close_button_y = 150 + offset_y

        self.close_rules_button_rect = (close_button_x - close_button_width // 2,
                                        close_button_y - close_button_height // 2,
                                        close_button_x + close_button_width // 2,
                                        close_button_y + close_button_height // 2)

        arcade.draw_rect_filled(arcade.rect.XYWH(close_button_x, close_button_y,
                                                 close_button_width, close_button_height),
                                RED)
        arcade.draw_rect_outline(arcade.rect.XYWH(close_button_x, close_button_y,
                                                  close_button_width, close_button_height),
                                 WHITE, 4)

        close_font_size = min(28, close_button_width // 10)
        arcade.draw_text("ЗАКРЫТЬ", close_button_x, close_button_y,
                         WHITE, close_font_size, anchor_x="center", anchor_y="center",
                         bold=True)

    def get_valid_moves(self, checker):
        moves = []
        row, col = checker.row, checker.col

        if checker.is_white or checker.is_king:
            for dr, dc in [(-1, -1), (-1, 1)]:
                new_row, new_col = row + dr, col + dc
                if self.is_valid_position(new_row, new_col) and not self.board[new_row][new_col]:
                    moves.append((new_row, new_col))

        if not checker.is_white or checker.is_king:
            for dr, dc in [(1, -1), (1, 1)]:
                new_row, new_col = row + dr, col + dc
                if self.is_valid_position(new_row, new_col) and not self.board[new_row][new_col]:
                    moves.append((new_row, new_col))

        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            if (checker.is_white and dr == 1 and not checker.is_king) or \
                    (not checker.is_white and dr == -1 and not checker.is_king):
                continue

            jump_row, jump_col = row + dr, col + dc
            land_row, land_col = row + 2 * dr, col + 2 * dc

            if (self.is_valid_position(jump_row, jump_col) and
                    self.is_valid_position(land_row, land_col) and
                    self.board[jump_row][jump_col] and
                    self.board[jump_row][jump_col].is_white != checker.is_white and
                    not self.board[land_row][land_col]):
                moves.append((land_row, land_col))

        return moves

    def is_valid_position(self, row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

    def on_update(self, delta_time):
        if self.game_over:
            self.update_particles()
            self.victory_timer += 1

            # Плавное появление сообщения
            if self.victory_message_alpha < 1.0:
                self.victory_message_alpha += delta_time * 2

            # Проигрываем звук победы один раз при появлении сообщения
            if self.victory_message_alpha > 0.1 and self.victory_timer < 10:
                self.sound_manager.play_victory_sound()

    def on_mouse_press(self, x, y, button, modifiers):
        current_width = self.width
        current_height = self.height
        square_size = min(current_width, current_height) // 14
        board_offset_x = (current_width - BOARD_SIZE * square_size) // 2
        board_offset_y = 150
        buttons_y = 50

        # Если игра окончена, обрабатываем кнопку в сообщении о победе
        if self.game_over and self.show_victory_message:
            if hasattr(self, 'victory_button_rect'):
                x1, y1, x2, y2 = self.victory_button_rect
                if x1 <= x <= x2 and y1 <= y <= y2:
                    self.setup_board()  # Начать новую игру
                    return

        if self.show_rules:
            if hasattr(self, 'close_rules_button_rect'):
                x1, y1, x2, y2 = self.close_rules_button_rect
                if x1 <= x <= x2 and y1 <= y <= y2:
                    self.show_rules = False
            return

        if hasattr(self, 'back_button_rect') and self.back_button_rect:
            x1, y1, x2, y2 = self.back_button_rect
            if x1 <= x <= x2 and y1 <= y <= y2:
                self.restart_program()
                return

        if hasattr(self, 'rules_button_rect'):
            x1, y1, x2, y2 = self.rules_button_rect
            if x1 <= x <= x2 and y1 <= y <= y2:
                self.show_rules = True
                return

        if hasattr(self, 'new_game_button_rect'):
            x1, y1, x2, y2 = self.new_game_button_rect
            if x1 <= x <= x2 and y1 <= y <= y2:
                self.setup_board()
                return

        # Если игра окончена, не обрабатываем клики по доске
        if self.game_over:
            return

        # Определяем, был ли клик в пределах доски
        col_idx = int((x - board_offset_x) // square_size)
        row_idx = int((y - board_offset_y) // square_size)

        is_on_board = (0 <= row_idx < BOARD_SIZE and 0 <= col_idx < BOARD_SIZE)

        board_left = board_offset_x
        board_right = board_offset_x + BOARD_SIZE * square_size
        board_bottom = board_offset_y
        board_top = board_offset_y + BOARD_SIZE * square_size

        is_in_board_area = (board_left <= x <= board_right and
                            board_bottom <= y <= board_top)

        checker = None
        if is_on_board:
            checker = self.board[row_idx][col_idx]

        # Если клик на шашку текущего игрока
        if checker and checker.is_white == self.current_player:
            self.selected_checker = checker
            self.valid_moves = self.get_valid_moves(checker)
            # Звук
            self.sound_manager.play_move_sound()

        elif self.selected_checker and is_on_board and (row_idx, col_idx) in self.valid_moves:
            self.make_move(self.selected_checker, row_idx, col_idx)

        else:
            if is_in_board_area and not is_on_board:
                self.selected_checker = None
                self.valid_moves = []
            elif is_on_board and checker and checker.is_white != self.current_player:
                self.sound_manager.play_move_sound()
                self.selected_checker = None
                self.valid_moves = []
            else:
                self.selected_checker = None
                self.valid_moves = []

        if hasattr(self, 'back_button_rect'):
            x1, y1, x2, y2 = self.back_button_rect
            if x1 <= x <= x2 and y1 <= y <= y2:
                self.restart_program()

                return

    def restart_program(self):
        # Плавно перезапускает программу
        import subprocess
        import sys
        import time

        # Закрываем окно arcade плавно
        self.close()
        # Запускаем новую копию программы
        try:
            python = sys.executable
            subprocess.Popen([python] + sys.argv)
        except Exception as e:
            pass

    def make_move(self, checker, new_row, new_col):
        old_row, old_col = checker.row, checker.col

        self.capture_made = False
        self.king_created = False

        # Проверяем, был ли это ход со взятием
        row_diff = abs(new_row - old_row)
        if row_diff == 2:
            mid_row = (old_row + new_row) // 2
            mid_col = (old_col + new_col) // 2
            if self.board[mid_row][mid_col]:
                self.board[mid_row][mid_col] = None
                if checker.is_white:
                    self.black_count -= 1
                else:
                    self.white_count -= 1
                self.capture_made = True

        # Перемещаем шашку
        self.board[new_row][new_col] = checker
        self.board[old_row][old_col] = None
        checker.row, checker.col = new_row, new_col
        self.move_count += 1

        if (checker.is_white and new_row == 0) or (not checker.is_white and new_row == BOARD_SIZE - 1):
            if not checker.is_king:  # Только если еще не дамка
                checker.is_king = True
                self.king_created = True

        if self.capture_made:
            self.sound_manager.play_capture_sound()
        elif self.king_created:
            self.sound_manager.play_king_sound()
        else:
            self.sound_manager.play_move_sound()
        self.check_game_over()

        if not self.game_over:
            self.current_player = not self.current_player
            self.selected_checker = None
            self.valid_moves = []

    def _save_game_result(self, winner):
        # Сохраняет результат игры в БД
        try:
            # Определяем счет
            if winner == "Белые":
                white_score = self.white_count
                black_score = 0
            else:
                white_score = 0
                black_score = self.black_count

            # Сохраняем в базу данных
            db.save_game(
                game_name="Русские шашки",
                winner=winner,
                white_score=white_score,
                black_score=black_score,
                moves_count=self.move_count
            )

        except Exception as e:
            pass

    def check_game_over(self):
        if self.white_count == 0:
            self.trigger_victory("black")
        elif self.black_count == 0:
            self.trigger_victory("white")

    def save_to_db(self, winner):
        game_name = "Русские шашки"
        date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

        # Просто сохраняем в БД
        db.save_game(game_name, winner, date)

        print(f"Сохранено в БД: {game_name} - {winner} - {date}")


class HistoryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("История игр")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        title = QLabel("История игр")
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Игра", "Победитель", "Дата"])
        layout.addWidget(self.table)

        btn_clear = QPushButton("Очистить историю")
        btn_clear.clicked.connect(self.clear_history)

        layout.addWidget(btn_clear)

        self.setLayout(layout)

        # Загружаем историю при открытии
        self.load_history()

    def load_history(self):
        # Просто загружает историю из БД
        games = db.get_all_games()

        self.table.setRowCount(len(games))

        for row, game in enumerate(games):
            self.table.setItem(row, 0, QTableWidgetItem(game[1]))  # Игра
            self.table.setItem(row, 1, QTableWidgetItem(game[2]))  # Победитель
            self.table.setItem(row, 2, QTableWidgetItem(game[3]))  # Дата

    def clear_history(self):
        # Очищает историю
        reply = QMessageBox.question(self, "Очистить",
                                     "Удалить всю историю?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            db.clear_history()
            self.load_history()


class NotWorkingMessage(QMessageBox):
    def __init__(self, parent=None, auto_show=True):
        super().__init__(parent)
        self.setWindowTitle("Информация")
        self.setText("К сожалению, это пока не разработано")
        self.setIcon(QMessageBox.Icon.Information)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)


def except_hook(csl, exception, traceback):
    sys.__excepthook__(csl, exception, traceback)


if __name__ == "__main__":
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = Main_Window()
    ex.showMaximized()
    sys.exit(app.exec())