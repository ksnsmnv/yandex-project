import sqlite3
import sys
import matplotlib.pyplot as plt
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.menu.clicked.connect(self.open_new_window)
        self.assess.clicked.connect(self.open_new_window)
        self.info.clicked.connect(self.open_new_window)
        self.changes.clicked.connect(self.open_new_window)

    def open_new_window(self):
        if self.sender() == self.menu:
            self.new_module = MenuWidget(self, "menu.ui")
        elif self.sender() == self.assess:
            self.new_module = AssessWidget(self, "assess.ui")
        elif self.sender() == self.info:
            self.new_module = InfoWidget(self, "info.ui")
        elif self.sender() == self.changes:
            self.new_module = ChangesWidget(self, "changes.ui")
        self.new_module.show()


class MenuWidget(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)
        self.con = sqlite3.connect('films_db.splite')
        self.CUR = self.con.cursor()
        self.WEEKDAYS = {'Пн': 'понедельник', 'Вт': 'вторник', 'Ср': 'среду', 'Чт': 'четверг',
                         'Пт': 'пятницу', 'Сб': 'субботу'}
        self.DAYS = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']
        data_in_dishes = [i[0] for i in
                          self.CUR.execute("SELECT dish FROM menu WHERE id in "
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
        self.buffet.triggered.connect(self.run_buffet)
        self.get.clicked.connect(self.open_dish_info)

    def run_buffet(self):
        data_in_dishes = [i[0] for i in
                          self.CUR.execute("SELECT dish FROM buffet").fetchall()]
        w = uic.loadUi('assess.ui')
        w.show()
        for i in range(len(data_in_dishes)):
            pass

    def run(self):
        self.title.setText(self.title.text()[:8] + self.WEEKDAYS[self.sender().text()])
        if self.sender().text() == 'Пн':
            data_in_dishes = [i[0] for i in
                              self.CUR.execute("SELECT dish FROM menu WHERE id in "
                                               "(SELECT id FROM menu_days WHERE id_weekdays = ?)", (1,)).fetchall()]
        elif self.sender().text() == 'Вт':
            data_in_dishes = [i[0] for i in
                              self.CUR.execute("SELECT dish FROM menu WHERE id in "
                                               "(SELECT id FROM menu_days WHERE id_weekdays = 2)").fetchall()]
        elif self.sender().text() == 'Ср':
            data_in_dishes = [i[0] for i in
                              self.CUR.execute("SELECT dish FROM menu WHERE id in "
                                               "(SELECT id FROM menu_days WHERE id_weekdays = 3)").fetchall()]
        elif self.sender().text() == 'Чт':
            data_in_dishes = [i[0] for i in
                              self.CUR.execute("SELECT dish FROM menu WHERE id in "
                                               "(SELECT id FROM menu_days WHERE id_weekdays = 4)").fetchall()]
        elif self.sender().text() == 'Пт':
            data_in_dishes = [i[0] for i in
                              self.CUR.execute("SELECT dish FROM menu WHERE id in "
                                               "(SELECT id FROM menu_days WHERE id_weekdays = 5)").fetchall()]
        elif self.sender().text() == 'Сб':
            data_in_dishes = [i[0] for i in
                              self.CUR.execute("SELECT dish FROM menu WHERE id in "
                                               "(SELECT id FROM menu_days WHERE id_weekdays = 6)").fetchall()]
        self.dish.setText(data_in_dishes[0])
        self.dish_2.setText(data_in_dishes[1])
        self.dish_3.setText(data_in_dishes[2])
        self.dish_4.setText(data_in_dishes[3])
        self.dish_5.setText(data_in_dishes[4])

    def open_dish_info(self):
        labels = ['proteins', 'fats', 'carbohydrates']
        sizes = 20, 60, 20 # подставить нужные значения
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels)
        ax1.axis('equal')
        plt.show()

    def initUI(self, args):
        uic.loadUi('menu.ui', self)


class AssessWidget(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        uic.loadUi('assess.ui', self)


class InfoWidget(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        uic.loadUi('info.ui', self)


class ChangesWidget(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)
        self.btn.clicked.connect(self.change_menu)
        
    def change_menu(self):
        self.con = sqlite3.connect('films_db.splite')
        self.cur = self.con.cursor()
        self.data_base = [i[0] for i in self.cur.execute("SELECT dish FROM menu").fetchall()]
        try:
            self.name = self.old_dish.text().strip()
            if self.name not in self.data_base:
                self.fer_errors.setText('Такого блюда нет в меню')
                return ''
            self.new_name = str(self.new_dish.text())       
            self.weight = float(self.lineEdit.text())
            self.calories = float(self.lineEdit_2.text())
            self.proteins = float(self.lineEdit_3.text())
            self.fats = float(self.lineEdit_4.text())
            self.carbohydrates = float(self.lineEdit_5.text())
            self.change_dish()
        except ValueError:
            self.for_errors.setText('Неправильный формат ввода')
        
    def change_dish(self):
        self.cur.execute("""UPDATE menu SET dish = ? WHERE dish = ?""", (self.new_name, self.name))
        self.con.commit()
        self.cur.execute("""UPDATE menu SET weight = ? WHERE dish = ?""", (self.weight, self.new_name))
        self.con.commit()
        self.cur.execute("""UPDATE menu SET calories = ? WHERE dish = ?""", (self.calories, self.new_name))
        self.cur.execute("""UPDATE menu SET proteins = ? WHERE dish = ?""", (self.proteins, self.new_name))
        self.con.commit()
        self.cur.execute("""UPDATE menu SET fat = ? WHERE dish = ?""", (self.fats, self.new_name))
        self.cur.execute("""UPDATE menu SET carbohudrates = ? WHERE dish = ?""", (self.carbohydrates, self.new_name))
        self.con.commit()

    def initUI(self, args):
        uic.loadUi('changes.ui', self)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
