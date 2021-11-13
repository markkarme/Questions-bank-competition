from os import name
from PyQt5 import QtWidgets,QtCore,QtGui, sip
from views import main_view
from PyQt5.QtWidgets import QSizeGrip
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtMultimedia import QMediaPlayer,QMediaContent
import random
from view_manager.TrueWidget import TrueWidget
from view_manager.FalseWidget import FalseWidget
import json
import time
class BankQuestion(main_view.Ui_MainWindow,QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        QSizeGrip(self.size_grip)
        self.current_page = 0

        #close btn
        self.close_window_btn.clicked.connect(self.close)
        self.minimize_window_btn.clicked.connect(self.showMinimized)
        #maxmim btn
        self.restore_btn.clicked.connect(self.restore_or_maxmize_window)
        def moveWindow(e):
            if self.isMaximized() == False:
                if e.buttons() == Qt.LeftButton:
                    self.move(self.pos()+e.globalPos()-self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
        self.header_frame.mouseMoveEvent = self.moveWindow
        # variables
        self.boys_items = -1
        self.girls_items = -1
        self.score = 0
        self.score_girls = 0
        self.random_choice = "0"
        self.chosen_button = 1

        self.true_song = QMediaPlayer()
        self.true_song.setMedia(QMediaContent(QtCore.QUrl("winners_ong.mpeg")))
        self.false_song = QMediaPlayer()
        self.false_song.setMedia(QMediaContent(QtCore.QUrl("loser_song.mpeg")))

        # question time variables
        self.question_time = 30
        self.player_time = self.question_time
        # question song
        self.question_song = QMediaPlayer()
        self.question_song.setMedia(QMediaContent(QtCore.QUrl("question_song.mp3")))
        # get question dic from questions file json
        json_file = open("questions.json")
        self.questions_dic = json.load(json_file)
        self.choices = [key for key in self.questions_dic.keys()]
        self.choose_from = self.choices.copy()
        # get player answer
        self.player_answer = ""
        ########################################################################
        # main code
        self.get_rand_number_btn.clicked.connect(self.get_random_number)
        self.back_btn.clicked.connect(self.display_previous_page)
        self.next_btn.clicked.connect(self.display_next_page)
        # config boys result
        self.boys_true_btn.clicked.connect(self.add_true_boys_widget)
        self.boys_false_btn.clicked.connect(self.add_false_boys_widget)
        # config girls result
        self.girls_true_btn.clicked.connect(self.add_true_girls_widget)
        self.girls_false_btn.clicked.connect(self.add_false_girls_widget)
        # config answers button
        self.answer_1_btn.clicked.connect(lambda: self.set_button_bk_color(self.answer_1_btn, 1))
        self.answer_2_btn.clicked.connect(lambda: self.set_button_bk_color(self.answer_2_btn, 2))
        self.answer_3_btn.clicked.connect(lambda: self.set_button_bk_color(self.answer_3_btn, 3))
        self.answer_4_btn.clicked.connect(lambda: self.set_button_bk_color(self.answer_4_btn, 4))
        # config result buttons
        self.boys_false_btn.setDisabled(True)
        self.boys_true_btn.setDisabled(True)
        self.girls_false_btn.setDisabled(True)
        self.girls_true_btn.setDisabled(True)
        self.boys_result_btn.clicked.connect(self.check_boys_answer)
        self.girls_result_btn.clicked.connect(self.check_girls_answer)

    # chcek answer function
    def check_boys_answer(self):
        print(self.player_answer , self.questions_dic[self.random_choice]["answer"])
        if self.player_answer == self.questions_dic[self.random_choice]["answer"]:
            self.add_true_boys_widget()
        else:
            self.add_false_boys_widget()
    def check_girls_answer(self):
        print(self.player_answer , self.questions_dic[self.random_choice]["answer"])
        if self.player_answer == self.questions_dic[self.random_choice]["answer"]:
            self.add_true_girls_widget()
        else:
            self.add_false_girls_widget()
    # config back ground answers button color
    def set_button_bk_color(self, button_opj,button_number):
        button_opj.setStyleSheet("background-color:  rgb(255, 179, 0);")
        self.player_answer = button_opj.text()
        self.chosen_button = button_number
        if button_number == 1:
            self.answer_2_btn.setDisabled(True)
            self.answer_3_btn.setDisabled(True)
            self.answer_4_btn.setDisabled(True)
        elif button_number == 2:
            self.answer_1_btn.setDisabled(True)
            self.answer_3_btn.setDisabled(True)
            self.answer_4_btn.setDisabled(True)
        elif button_number == 3:
            self.answer_1_btn.setDisabled(True)
            self.answer_2_btn.setDisabled(True)
            self.answer_4_btn.setDisabled(True)
        elif button_number == 4:
            self.answer_1_btn.setDisabled(True)
            self.answer_2_btn.setDisabled(True)
            self.answer_3_btn.setDisabled(True)
    # true widget function that add widget to boys layout
    def add_true_boys_widget(self):
        self.true_song.play()
        self.boys_items += 1
        true_widget = TrueWidget()
        true_widget.pushButton_7.clicked.connect(lambda: self.remove_widget_boys_layout("True"))
        self.boys_layout.addWidget(true_widget)
        self.score = self.score + 1
        self.boys_score_lbl.setText(f"Score: {self.score}")

    # false widget function that add widget to boys layout
    def add_false_boys_widget(self):
        self.false_song.play()
        self.boys_items += 1
        false_widget = FalseWidget()
        false_widget.pushButton_6.clicked.connect(lambda: self.remove_widget_boys_layout("False"))
        self.boys_layout.addWidget(false_widget)
        self.score = self.score - 1
        self.boys_score_lbl.setText(f"Score: {self.score}")

    def remove_widget_boys_layout(self,wich):
        self.boys_layout.itemAt(self.boys_items).widget().deleteLater()
        self.boys_items -=1
        if wich == "False":
            self.score = self.score + 1
            self.boys_score_lbl.setText(f"Score: {self.score}")
        if self.boys_items == -1:
            self.boys_score_lbl.setText(f"Score: 0")
            self.score = 0

    # true widget function that add widget to girls layout
    def add_true_girls_widget(self):
        self.true_song.play()
        self.girls_items += 1
        true_widget = TrueWidget()
        true_widget.pushButton_7.clicked.connect(lambda: self.remove_widget_girls_layout("True"))
        self.girls_layout.addWidget(true_widget)
        self.score_girls = self.score_girls + 1
        self.girls_score_lbl.setText(f"Score: {self.score_girls}")

    # false widget function that add widget to boys layout
    def add_false_girls_widget(self):
        self.false_song.play()
        self.girls_items += 1
        false_widget = FalseWidget()
        false_widget.pushButton_6.clicked.connect(lambda: self.remove_widget_girls_layout("False"))
        self.girls_layout.addWidget(false_widget)
        self.score_girls = self.score_girls - 1
        self.girls_score_lbl.setText(f"Score: {self.score_girls}")

    def remove_widget_girls_layout(self, wich):
        self.girls_layout.itemAt(self.girls_items).widget().deleteLater()
        self.girls_items -= 1
        if wich == "False":
            self.score_girls = self.score_girls + 1
            self.girls_score_lbl.setText(f"Score: {self.score_girls}")
        if self.girls_items == -1:
            self.girls_score_lbl.setText(f"Score: 0")
            self.score_girls = 0

    def get_random_number(self):
        try:
            self.get_rand_number_btn.setDisabled(True)
            self.random_choice = random.choice(self.choose_from)
            self.rand_number_lcd.display(self.random_choice)
            self.question_lbl.setText(self.questions_dic[self.random_choice]["question"])
            self.answer_1_btn.setText(self.questions_dic[self.random_choice]["choices"][0].lower())
            self.answer_2_btn.setText(self.questions_dic[self.random_choice]["choices"][1].lower())
            self.answer_3_btn.setText(self.questions_dic[self.random_choice]["choices"][2].lower())
            self.answer_4_btn.setText(self.questions_dic[self.random_choice]["choices"][3].lower())
            self.choose_from.remove(self.random_choice)
        except:
            self.display_info_dialog("finish","The game ended")
        # self.number_lbl.setText(random.choice(["1","2","3","5","4"]))
    def config_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_time)
        self.timer.start(1000)
    def show_time(self):
        self.player_time -= 1
        self.timer_lbl.setText(str(self.player_time))
        if self.player_time == 0:
            self.timer.stop()


    def display_info_dialog(self, title, body):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(body)
        msg.exec_()
    
    def display_previous_page(self):
        self.next_btn.setDisabled(True)
        self.current_page = self.current_page - 1
        if self.current_page < 0:
            self.current_page = 0
        self.stackedWidget.setCurrentIndex(self.current_page)
        if self.current_page == 0:
            self.next_btn.setEnabled(True)
            self.set_button_style(self.answer_1_btn)
            self.set_button_style(self.answer_2_btn)
            self.set_button_style(self.answer_3_btn)
            self.set_button_style(self.answer_4_btn)
        right_answer = self.questions_dic[self.random_choice]["answer"]
        if self.current_page == 1:
            self.get_rand_number_btn.setEnabled(True)
            if self.answer_1_btn.text() == right_answer:
                self.answer_1_btn.setStyleSheet("background-color: rgb(4, 221, 40);")
                self.answer_2_btn.setStyleSheet("background-color: rgb(24, 24, 36);")
                self.answer_3_btn.setStyleSheet("background-color: rgb(24, 24, 36);")
                self.answer_4_btn.setStyleSheet("background-color: rgb(24, 24, 36);")
            elif self.answer_2_btn.text() == right_answer:
                self.answer_2_btn.setStyleSheet("background-color: rgb(4, 221, 40);")
                self.answer_1_btn.setStyleSheet("background-color: rgb(24, 24, 36);")
                self.answer_3_btn.setStyleSheet("background-color: rgb(24, 24, 36);")
                self.answer_4_btn.setStyleSheet("background-color: rgb(24, 24, 36);")
            elif self.answer_3_btn.text() == right_answer:
                self.answer_3_btn.setStyleSheet("background-color: rgb(4, 221, 40);")
                self.answer_1_btn.setStyleSheet("background-color: rgb(24, 24, 36);")
                self.answer_2_btn.setStyleSheet("background-color: rgb(24, 24, 36);")
                self.answer_4_btn.setStyleSheet("background-color: rgb(24, 24, 36);")
            elif self.answer_4_btn.text() == right_answer:
                self.answer_4_btn.setStyleSheet("background-color: rgb(4, 221, 40);")
                self.answer_1_btn.setStyleSheet("background-color: rgb(24, 24, 36);")
                self.answer_3_btn.setStyleSheet("background-color: rgb(24, 24, 36);")
                self.answer_2_btn.setStyleSheet("background-color: rgb(24, 24, 36);")

    def set_button_style(self, button):
        button.setEnabled(True)
        button.setStyleSheet("""
        QPushButton{background-color: rgb(24, 24, 36);
        QPushButton:hover{background-color: rgb(85, 170, 255);}""")

    def display_next_page(self):
        self.back_btn.setEnabled(False)
        self.current_page = self.current_page + 1
        if self.current_page > 2:
            self.current_page = 2
        self.stackedWidget.setCurrentIndex(self.current_page)
        if self.current_page == 1:
            self.player_time = self.question_time
            self.timer_lbl.setText(str(self.player_time))
            self.config_timer()
            self.question_song.play()
            # config specific

        if self.current_page == 2:
            self.timer.stop()
            del self.timer
            self.question_song.stop()
            self.back_btn.setEnabled(True)
            self.next_btn.setEnabled(False)

    def moveWindow(self,e):
        if self.isMaximized() == False:
            if e.buttons() == Qt.LeftButton:
                self.move(self.pos()+e.globalPos()-self.clickPosition)
                self.clickPosition = e.globalPos()
                e.accept()
    def mousePressEvent(self,event):
        self.clickPosition = event.globalPos()
    def restore_or_maxmize_window(self):
        if self.isMaximized():
            self.showNormal()
            #change icon
            self.restore_btn.setIcon(QtGui.QIcon(u":/icons/icons/maximize-2.svg"))
        else:
            self.showMaximized()
            self.restore_btn.setIcon(QtGui.QIcon(u":/icons/icons/minimize-2.svg"))