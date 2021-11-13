import sqlite3
import sys
from statistics import mean
import datetime
import matplotlib.pyplot as plt
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog
CON = sqlite3.connect('films_db.splite')
CUR = CON.cursor()
WEEKDAYS = {'Пн': 'понедельник', 'Вт': 'вторник', 'Ср': 'среду', 'Чт': 'четверг',
            'Пт': 'пятницу', 'Сб': 'субботу'}
WEEK = ['понедельник', 'вторник', 'среду', 'четверг', 'пятницу', 'субботу']


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
            self.new_module.show()
        elif self.sender() == self.assess:
            self.new_module = AssessWidget(self, "assess.ui")
            self.new_module.show()
        elif self.sender() == self.info:
            self.new_module = InfoWidget(self, "info.ui")
            self.new_module.show()
        elif self.sender() == self.changes:
            self.entering_password()

    def entering_password(self):
        password, ok_pressed = QInputDialog.getText(
            self, "Ввод пароля", "Введите пароль доступа:")
        if password == '123456789' and ok_pressed:
            self.new_module = ChangesWidget(self, "changes.ui")
            self.new_module.show()
        elif ok_pressed:
            self.entering_password()
        else:
            return
            

class MenuWidget(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)
        self.set_today_menu()
        self.mon.triggered.connect(self.run)
        self.tue.triggered.connect(self.run)
        self.wed.triggered.connect(self.run)
        self.thu.triggered.connect(self.run)
        self.fri.triggered.connect(self.run)
        self.sat.triggered.connect(self.run)
        self.get.clicked.connect(self.open_dish_info)
        self.information.clicked.connect(self.open_dish_info)
        self.set_buffet()
        
    def set_today_menu(self):
        day = datetime.datetime.now().isoweekday() - 1
        if day == 6:
            day = 0
        self.title.setText(self.title.text()[:8] + WEEK[day])
        data_in_dishes = [i[0] for i in
                          CUR.execute("SELECT dish FROM menu WHERE id in "
                                      "(SELECT id FROM menu_days WHERE id_weekdays = ?)", (day,)).fetchall()]
        self.dish.setText(data_in_dishes[0])
        self.dish_2.setText(data_in_dishes[1])
        self.dish_3.setText(data_in_dishes[2])
        self.dish_4.setText(data_in_dishes[3])
        self.dish_5.setText(data_in_dishes[4])

        # добавление списка блюд в списке
    def set_buffet(self):
        all_dishes = [i[0] for i in CUR.execute('SELECT dish FROM buffet').fetchall()]
        self.buffet_dish.addItems(all_dishes)

    # получение меню в соответствии с днями недели
    def run(self):
        self.title.setText(self.title.text()[:8] + WEEKDAYS[self.sender().text()])
        if self.sender().text() == 'Пн':
            data_in_dishes = [i[0] for i in
                              CUR.execute("SELECT dish FROM menu WHERE id in "
                                          "(SELECT id FROM menu_days WHERE id_weekdays = ?)", (1,)).fetchall()]
        elif self.sender().text() == 'Вт':
            data_in_dishes = [i[0] for i in
                              CUR.execute("SELECT dish FROM menu WHERE id in "
                                          "(SELECT id FROM menu_days WHERE id_weekdays = 2)").fetchall()]
        elif self.sender().text() == 'Ср':
            data_in_dishes = [i[0] for i in
                              CUR.execute("SELECT dish FROM menu WHERE id in "
                                          "(SELECT id FROM menu_days WHERE id_weekdays = 3)").fetchall()]
        elif self.sender().text() == 'Чт':
            data_in_dishes = [i[0] for i in
                              CUR.execute("SELECT dish FROM menu WHERE id in "
                                          "(SELECT id FROM menu_days WHERE id_weekdays = 4)").fetchall()]
        elif self.sender().text() == 'Пт':
            data_in_dishes = [i[0] for i in
                              CUR.execute("SELECT dish FROM menu WHERE id in "
                                          "(SELECT id FROM menu_days WHERE id_weekdays = 5)").fetchall()]
        elif self.sender().text() == 'Сб':
            data_in_dishes = [i[0] for i in
                              CUR.execute("SELECT dish FROM menu WHERE id in "
                                          "(SELECT id FROM menu_days WHERE id_weekdays = 6)").fetchall()]
        self.dish.setText(data_in_dishes[0])
        self.dish_2.setText(data_in_dishes[1])
        self.dish_3.setText(data_in_dishes[2])
        self.dish_4.setText(data_in_dishes[3])
        self.dish_5.setText(data_in_dishes[4])

    def open_dish_info(self):
        if self.sender().text() == 'Просмотреть информацию о блюде':
            meal = self.button_group.checkedButton().text()
            table = 'menu'
        else:
            meal = self.buffet_dish.currentText()
            table = 'buffet'

        labels = ['proteins', 'fats', 'carbohydrates']
        if table == 'menu':
            proteins = [i[0] for i in
                        CUR.execute("SELECT proteins FROM menu WHERE dish = ?",
                                    (meal,)).fetchall()]
            fats = [i[0] for i in
                    CUR.execute("SELECT fat FROM menu WHERE dish = ?",
                                (meal,)).fetchall()]
            carbs = [i[0] for i in
                     CUR.execute("""SELECT carbohudrates 
                                             FROM menu WHERE dish = ?""", (meal,)).fetchall()]
        else:
            proteins = [i[0] for i in
                        CUR.execute("SELECT poteins FROM buffet WHERE dish = ?",
                                    (meal,)).fetchall()]
            fats = [i[0] for i in
                    CUR.execute("SELECT fats FROM buffet WHERE dish = ?",
                                (meal,)).fetchall()]
            carbs = [i[0] for i in
                     CUR.execute("""SELECT carbohydrates 
                                             FROM buffet WHERE dish = ?""", (meal,)).fetchall()]
        try:
            sizes = float(proteins[0]), float(fats[0]), float(carbs[0])
        # если запятая вместо точки
        except ValueError:
            proteins[0], fats[0], carbs[0] = str(proteins[0]), str(fats[0]), str(carbs[0])
            if ',' in proteins[0]:
                proteins[0] = proteins[0][:proteins[0].find(',')] + '.' + proteins[0][proteins[0].find(',') + 1:]
            if ',' in fats[0]:
                fats[0] = fats[0][:fats[0].find(',')] + '.' + fats[0][fats[0].find(',') + 1:]
            if ',' in carbs[0]:
                carbs[0] = carbs[0][:carbs[0].find(',')] + '.' + carbs[0][carbs[0].find(',') + 1:]
            sizes = float(proteins[0]), float(fats[0]), float(carbs[0])
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
        self.set_min_max()
        self.set_dishes()
        self.dish.addItems(self.all_dishes)
        self.dish_2.addItems(self.all_dishes)
        self.dish_3.addItems(self.all_dishes)
        self.dish_4.addItems(self.all_dishes)
        self.dish_5.addItems(self.all_dishes)
        self.send.clicked.connect(self.sending)
        self.cafe.clicked.connect(self.set_dishes)
        self.lunch.clicked.connect(self.set_dishes)
    # установка мин. и макс. на spinbox

    def set_min_max(self):
        self.number_b.setMinimum(1)
        self.number_l.setMinimum(1)
        self.number_b.setMaximum(5)
        self.number_l.setMaximum(5)
        self.spn.setMinimum(1)
        self.spn.setMaximum(5)
        self.spn_2.setMinimum(1)
        self.spn_2.setMaximum(5)
        self.spn_3.setMinimum(1)
        self.spn_3.setMaximum(5)
        self.spn_4.setMinimum(1)
        self.spn_4.setMaximum(5)
        self.spn_5.setMinimum(1)
        self.spn_5.setMaximum(5)

    # добавление выпадающих списков
    def set_dishes(self):
        self.all_dishes = ['']
        self.all_dishes.extend([i[0] for i in CUR.execute('SELECT dish FROM menu').fetchall()])
        self.where = self.number_l.text()
        if self.sender().text() == 'Буфет':
            self.all_dishes = ['']
            self.all_dishes.extend([i[0] for i in CUR.execute('SELECT dish FROM buffet').fetchall()])
            print(self.all_dishes)
            self.where = self.number_b.text()
        if self.where == '1':
            self.dish.clear()
            self.dish.addItems(self.all_dishes)
            self.mistake.clear()
        elif self.where == '2':
            self.dish_2.clear()
            self.dish_2.addItems(self.all_dishes)
            self.mistake.clear()
        elif self.where == '3':
            self.dish_3.clear()
            self.dish_3.addItems(self.all_dishes)
            self.mistake.clear()
        elif self.where == '4':
            self.dish_4.clear()
            self.dish_4.addItems(self.all_dishes)
            self.mistake.clear()
        else:
            self.dish_5.clear()
            self.dish_5.addItems(self.all_dishes)
            self.mistake.clear()
    
    def sending(self):
        file = open('feedback.txt', 'r')
        try:
            self.feedback = file.read() + '\n'
        except:
            self.feedback = ''
        if self.dish.currentText() != '':
            self.feedback += str(self.dish.currentText() + ' ' + str(self.spn.value()) + '\n')
        if self.dish.currentText() != '':
            self.feedback += str(self.dish_2.currentText() + ' ' + str(self.spn_2.value()) + '\n')
        if self.dish.currentText() != '':
            self.feedback += str(self.dish_3.currentText() + ' ' + str(self.spn_3.value()) + '\n')
        if self.dish.currentText() != '':
            self.feedback += str(self.dish_4.currentText() + ' ' + str(self.spn_4.value()) + '\n')
        if self.dish.currentText() != '':
            self.feedback += str(self.dish_5.currentText() + ' ' + str(self.spn_5.value()) + '\n')
        file = open('feedback.txt', 'w')
        file.write(self.feedback)
        file.close()
        file = open('feedback.txt')

    def initUI(self, args):
        uic.loadUi('assess.ui', self)


class InfoWidget(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)
        self.textEdit.setText(self.set_text())

    def set_text(self):
        try:
            file = open('feedback.txt', 'r')
            data = file.read().split('\n')
            info = {}
            for i in data:
                if i[:-2] in info:
                    info[i[:-2]].append(int(i[-1]))
                else:
                    info[i[:-2]] = [int(i[-1])]
            for i in info:
                info[i] = round(mean(info[i]), 2)
            popular = sorted(info, key=lambda x: info[x], reverse=True)
            answer_to_return = ''
            for i in popular:
                answer_to_return += i + ' ' + str(info[i]) + '\n'
            return answer_to_return
        except FileNotFoundError:
            return 'Информации пока нет.'

    def initUI(self, args):
        uic.loadUi('feedback.ui', self)


class ChangesWidget(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)
        self.table = 'menu'
        self.btn.clicked.connect(self.set_table)
        self.menu.triggered.connect(self.run)
        self.menu_2.triggered.connect(self.run)

    # установка таблицы, в которой будут происходить изменения
    def run(self):
        print(1)
        if self.sender().text() == 'Cтоловая':
            self.title = self.title[:16] + 'столовой'
            self.table = 'menu'
            print('столовая')
        else:
            self.title = self.title[:16] + 'буфета'
            self.table == 'buffet'
            print('буфет')
            
    # изменеия в таблице буфета
    def change_buf(self):
        self.cur.execute("""UPDATE buffet SET dish = ? WHERE dish = ?""", (self.new_name, self.name))
        self.con.commit()
        self.cur.execute("""UPDATE buffet SET weight = ? WHERE dish = ?""", (self.weight, self.new_name))
        self.con.commit()
        self.cur.execute("""UPDATE buffet SET calories = ? WHERE dish = ?""", (self.calories, self.new_name))
        self.cur.execute("""UPDATE buffet SET poteins = ? WHERE dish = ?""", (self.proteins, self.new_name))
        self.con.commit()
        self.cur.execute("""UPDATE buffet SET fats = ? WHERE dish = ?""", (self.fats, self.new_name))
        self.cur.execute("""UPDATE buffet SET carbohydrates = ? WHERE dish = ?""", (self.carbohydrates, self.new_name))
        self.con.commit()

    def set_table(self):
        if self.table == 'menu':
            self.change_menu()
        else:
            self.change_buffet()

    def change_menu(self):
        self.data_base = [i[0] for i in CUR.execute("SELECT dish FROM menu").fetchall()]
        self.change()

    def change_buffet(self):
        self.data_base = [i[0] for i in CUR.execute("SELECT buffet FROM menu").fetchall()]
        self.change()

    def change(self):
        try:
            self.name = self.old_dish.text().strip()
            if self.name not in self.data_base:
                self.for_errors.setText('Такого блюда нет в меню')
                return ''
            self.new_name = str(self.new_dish.text())
            self.weight = float(self.lineEdit.text())
            self.calories = float(self.lineEdit_2.text())
            self.proteins = float(self.lineEdit_3.text())
            self.fats = float(self.lineEdit_4.text())
            self.carbohydrates = float(self.lineEdit_5.text())
            if self.table == 'menu':
                self.change_dish()
            else:
                self.change_buf()
        except ValueError:
            self.for_errors.setText('Неправильный формат ввода')

    # изменения в таблице меню
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