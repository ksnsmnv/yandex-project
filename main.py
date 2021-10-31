import sqlite3
import sys
import matplotlib.pyplot as plt
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect('films_db.splite')
        self.cur = self.con.cursor()
        uic.loadUi('menu.ui', self)
        self.weekdays = {'Пн': 'понедельник', 'Вт': 'вторник', 'Ср': 'среду', 'Чт': 'четверг',
                         'Пт': 'пятницу', 'Сб': 'субботу'}
        # работа с виджетом "Меню" (+ "run")
        data_in_dishes = [i[0] for i in
                          self.cur.execute("SELECT dish FROM menu WHERE id in "
                                           "(SELECT id FROM menu_days WHERE id_weekdays = 1)").fetchall()]
        self.dish.setText(data_in_dishes[0])
        self.dish_2.setText(data_in_dishes[1])
        self.dish_3.setText(data_in_dishes[2])
        self.dish_4.setText(data_in_dishes[3])
        self.dish_5.setText(data_in_dishes[4])
        self.mon.triggered.connect(self.run)
        self.tue.triggered.connect(self.run)
        self.wed.triggered.connect(self.run)
        self.thu.triggered.connect(self.run)
        self.fri.triggered.connect(self.run)
        self.sat.triggered.connect(self.run)
        # self.buffet.triggered.connect(self.run)
        self.get.clicked.connect(self.open_dish_info)

    def run(self):
        self.title.setText(self.title.text()[:8] + self.weekdays[self.sender().text()])
        if self.sender().text() == 'Пн':
            data_in_dishes = [i[0] for i in
                              self.cur.execute("SELECT dish FROM menu WHERE id in "
                                               "(SELECT id FROM menu_days WHERE id_weekdays = 1)").fetchall()]
        elif self.sender().text() == 'Вт':
            data_in_dishes = [i[0] for i in
                              self.cur.execute("SELECT dish FROM menu WHERE id in "
                                               "(SELECT id FROM menu_days WHERE id_weekdays = 2)").fetchall()]
        elif self.sender().text() == 'Ср':
            data_in_dishes = [i[0] for i in
                              self.cur.execute("SELECT dish FROM menu WHERE id in "
                                               "(SELECT id FROM menu_days WHERE id_weekdays = 3)").fetchall()]
        elif self.sender().text() == 'Чт':
            data_in_dishes = [i[0] for i in
                              self.cur.execute("SELECT dish FROM menu WHERE id in "
                                               "(SELECT id FROM menu_days WHERE id_weekdays = 4)").fetchall()]
        elif self.sender().text() == 'Пт':
            data_in_dishes = [i[0] for i in
                              self.cur.execute("SELECT dish FROM menu WHERE id in "
                                               "(SELECT id FROM menu_days WHERE id_weekdays = 5)").fetchall()]
        elif self.sender().text() == 'Сб':
            data_in_dishes = [i[0] for i in
                              self.cur.execute("SELECT dish FROM menu WHERE id in "
                                               "(SELECT id FROM menu_days WHERE id_weekdays = 6)").fetchall()]
        self.dish.setText(data_in_dishes[0])
        self.dish_2.setText(data_in_dishes[1])
        self.dish_3.setText(data_in_dishes[2])
        self.dish_4.setText(data_in_dishes[3])
        self.dish_5.setText(data_in_dishes[4])

    def open_dish_info(self):
        labels = 'Cricket', 'Football', 'Hockey', 'F1'
        sizes = [15, 30, 45, 10]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels)
        ax1.axis('equal')
        plt.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
