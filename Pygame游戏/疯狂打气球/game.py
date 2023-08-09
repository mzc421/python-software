# -*- coding:utf-8 -*-
# @author: 木子川
# @Email:  m21z50c71@163.com
# @QQ交流群：830200766
# @QQ个人：2463739729

import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer


class BalloonShooterGame(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题为"疯狂打气球"，并将窗口位置设定在(100, 100)，大小为800x600像素
        self.setWindowTitle("疯狂打气球")
        self.setGeometry(100, 100, 800, 600)

        # 初始化得分和剩余时间为0和30
        self.score = 0
        self.time_remaining = 30

        # 创建垂直布局管理器layout和中央控件central_widget，并将布局管理器设置为中央控件的布局。然后将中央控件设置为窗口的中央控件
        self.layout = QVBoxLayout()
        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # 创建水平布局管理器score_layout和标签label_score，将标签对齐方式设置为右对齐，并设置标签的样式为字号24px。
        # 然后调用update_score方法更新得分标签的文本
        self.score_layout = QHBoxLayout()
        self.label_score = QLabel(self)
        self.label_score.setAlignment(Qt.AlignRight)
        self.label_score.setStyleSheet("font-size: 24px;")
        self.update_score()

        # 创建标签label_time，将标签对齐方式设置为左对齐，并设置标签的样式为字号24px。然后调用update_time方法更新剩余时间标签的文本。
        self.label_time = QLabel(self)
        self.label_time.setAlignment(Qt.AlignLeft)
        self.label_time.setStyleSheet("font-size: 24px;")
        self.update_time()

        # 将得分和剩余时间标签添加到水平布局管理器
        self.score_layout.addWidget(self.label_score)
        self.score_layout.addWidget(self.label_time)

        # 将水平布局管理器添加到垂直布局管理器
        self.layout.addLayout(self.score_layout)

        # 创建一个标签控件balloon，设置文本为"🎈"，样式为字号36px，并设置其位置和大小。
        # 然后将控件的mousePressEvent事件绑定到hit_balloon方法
        self.balloon = QLabel(self)
        self.balloon.setText("🎈")
        self.balloon.setStyleSheet("font-size: 36px;")
        self.balloon.setGeometry(400, 300, 50, 50)
        self.balloon.mousePressEvent = self.hit_balloon

        # 创建一个定时器timer，每隔1.1秒触发一次timeout信号，并将其连接到update_game方法上。然后启动定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(1100)

    def update_game(self):
        """
        在每次定时器触发时更新剩余时间并调用update_time方法。如果剩余时间小于等于0，则停止定时器。然后生成随机坐标，并将气球移动到相应位置
        :return:
        """
        self.time_remaining -= 1
        self.update_time()

        if self.time_remaining <= 0:
            self.timer.stop()

        x = random.randint(50, 700)
        y = random.randint(50, 500)
        self.balloon.move(x, y)

    def hit_balloon(self, event):
        """
        在点击气球时更新得分，并调用update_score方法
        :param event:
        :return:
        """
        self.score += 1
        self.update_score()

    def update_score(self):
        """
        更新得分标签的文本
        :return:
        """
        self.label_score.setText(f"得分: {self.score}")

    def update_time(self):
        """
        更新剩余时间标签的文本
        :return:
        """
        self.label_time.setText(f"剩余时间: {self.time_remaining} 秒")

    def keyPressEvent(self, event):
        """
        重写了keyPressEvent方法，当按下Esc键时关闭窗口
        :param event:
        :return:
        """
        if event.key() == Qt.Key_Escape:
            self.close()

    def mousePressEvent(self, event):
        """
        重写了mousePressEvent方法，当鼠标点击窗口时关闭窗口
        :param event:
        :return:
        """
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = BalloonShooterGame()
    game.show()
    sys.exit(app.exec_())


