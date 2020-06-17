# -*- coding: utf-8 -*-
"""
@author: GitHub@Oscarshu0719
"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QAction, QComboBox, QFileDialog, QHBoxLayout, 
                             QLabel, QMainWindow, QPushButton, QShortcut,  
                             QSlider, QStyle, QVBoxLayout, QWidget)
import sys
from src.thread import Thread

class VideoWindow(QMainWindow):
    """ Class:
    Video player window.
    """
    
    # Main window size.
    WIN_SIZE = [800, 600]
    
    def __init__(self, parent=None):
        """ Function:
        Setup user interface of Video player window.
        """
        
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("Video player") 
        self.resize(VideoWindow.WIN_SIZE[0], VideoWindow.WIN_SIZE[1])
        self.setWindowIcon(
                    self.style().standardIcon(QStyle.SP_DriveDVDIcon))
        
        self.video_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.record_start_time = None
        self.record_end_time = None
        self.video_name = ""

        self.widget_video = QVideoWidget()
        
        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.button_play = QPushButton()
        self.button_play.setEnabled(False)
        self.button_play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.button_play.clicked.connect(self.play_video)

        self.video_slider = QSlider(Qt.Horizontal)
        self.video_slider.setRange(0, 0)
        self.video_slider.sliderMoved.connect(self.set_position)
        self.video_duration = 0

        # Action 'Open'.
        self.action_open = QAction(QIcon('open.png'), '&Open', self)        
        self.action_open.setShortcut('Ctrl+O')
        self.action_open.setStatusTip('Open a video')
        self.action_open.triggered.connect(self.open_video)

        # Menu bar.
        self.menu_bar = self.menuBar()
        self.menu_menu = self.menu_bar.addMenu('&Menu')
        self.menu_menu.addAction(self.action_open)

        # Widget.
        self.widget_window = QWidget(self)
        self.setCentralWidget(self.widget_window)

        self.layout_operation = QHBoxLayout()
        self.layout_operation.setContentsMargins(0, 0, 0, 0)
        self.label_rotate = QLabel('Degree of rotation')
        self.combobox_degree = QComboBox()
        degrees = ['0', '90', '180', '270']
        self.combobox_degree.addItems(degrees)
        self.button_subclip_video = QPushButton('Subclip (Video)')
        self.button_subclip_audio = QPushButton('Subclip (Audio)')
        self.layout_operation.addWidget(self.label_rotate)
        self.layout_operation.addWidget(self.combobox_degree)
        self.layout_operation.addWidget(self.button_subclip_video)
        self.layout_operation.addWidget(self.button_subclip_audio)

        self.layout_record = QHBoxLayout()
        self.layout_record.setContentsMargins(0, 0, 0, 0)
        self.button_start = QPushButton('Start')
        self.button_end = QPushButton('End')
        self.button_clear = QPushButton('Clear')
        self.layout_record.addWidget(self.button_start)
        self.layout_record.addWidget(self.button_end)
        self.layout_record.addWidget(self.button_clear)

        self.button_start.clicked.connect(self.record_start)
        self.button_end.clicked.connect(self.record_end)
        self.button_subclip_video.clicked.connect(self.record_subclip_video)
        self.button_subclip_audio.clicked.connect(self.record_subclip_audio)
        self.button_clear.clicked.connect(self.record_clear)

        # Widget layout.
        self.layout_widget = QHBoxLayout()
        self.layout_widget.setContentsMargins(0, 0, 0, 0)
        self.layout_widget.addWidget(self.button_play)
        self.layout_widget.addWidget(self.video_slider)

        self.layout_window = QVBoxLayout()
        self.layout_window.addWidget(self.widget_video)
        self.layout_window.addLayout(self.layout_record)
        self.layout_window.addLayout(self.layout_operation)
        self.layout_window.addLayout(self.layout_widget)

        # Window layout.
        self.widget_window.setLayout(self.layout_window)

        self.video_player.setVideoOutput(self.widget_video)
        self.video_player.stateChanged.connect(self.media_state_changed)
        self.video_player.positionChanged.connect(self.position_changed)
        self.video_player.durationChanged.connect(self.duration_changed)
        self.video_player.error.connect(self.error_control)
        
#        QShortcut(Qt.Key_Up, self, self.arrow_up)
#        QShortcut(Qt.Key_Down, self, self.arrow_down)
        QShortcut(Qt.Key_Left, self, self.arrow_left_event)
        QShortcut(Qt.Key_Right, self, self.arrow_right_event)
        QShortcut(Qt.Key_Space, self, self.play_video)
        
#    def arrow_up(self):
#        print("up")
#
#    def arrow_down(self):
#        print("down")
    
    def arrow_left_event(self):
        """ Slot function:
        Action after the key 'arrow left' is pressed.
        Fast-forward to 10 seconds later.
        """
        
        self.set_position(self.video_slider.value() - 10 * 1000)

    def arrow_right_event(self):
        """ Slot function:
        Action after the key 'arrow right' is pressed.
        Go back to 10 seconds ago.
        """
        
        self.set_position(self.video_slider.value() + 10 * 1000)
    
    def mousePressEvent(self, event):
        """ Slot function:
        The starting position of the slider is 50.
        Note: This function still can't not accurately move the slider to the 
        clicked position.
        """

        slider_start_pos = 51
        if 42 <= self.height() - event.pos().y() <= 62:
            position = slider_start_pos + self.video_slider.minimum() + (event.pos().x() - slider_start_pos) / self.video_slider.width() * self.video_duration
            if position != self.video_slider.sliderPosition():
                self.set_position(position)
        
#    def keyPressEvent(self, event):
#        if event.key() == Qt.Key_A:
#            print(self.video_slider.value())
#        elif event.key() == Qt.Key_D:
#            print(self.video_slider.value())
            
    def closeEvent(self, event):
        """ Slot function:
        After clicking the 'close' button, pause the video.
        """

        self.video_player.pause()
        self.hide()
#        self.setVisible(False)
        
    def open_video(self):
        """ Slot function:
        Open a video from the file system.
        """
        
        video_name, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())
        self.video_name = video_name

        if video_name != '':
            self.video_player.setMedia(
                    QMediaContent(QUrl.fromLocalFile(video_name)))
#            self.setVisible(True)
            self.button_play.setEnabled(True)
            self.video_player.play()
        
            index = video_name.rfind('/')
            self.statusbar.showMessage(
                    "Info: Playing the video '" + video_name[(index + 1):] 
                    + "' ...")
            
    def double_clicked_play_video(self, video_name):
        """ Function:
        After double clicking, start playing the clicked video.
        """
        
        self.video_player.setMedia(
                QMediaContent(QUrl.fromLocalFile(video_name)))
        self.show()
        self.button_play.setEnabled(True)
        self.video_player.play()
        
        index = video_name.rfind('/')
        print(video_name)
        self.statusbar.showMessage(
                "Info: Playing the video '" + video_name[(index + 1):] 
                + "' ...")

    def play_video(self):
        """ Slot function:
        The slot function for the 'play' button.
        If the video player is currently paused, then play the video; 
        otherwise, pause the video.
        """
        
        if self.video_player.state() == QMediaPlayer.PlayingState:
            self.video_player.pause()
        else:
            self.video_player.play()

    def media_state_changed(self, state):
        """ Slot function:
        If the playing state changes, change the icon for the 'play' button.
        If the video player is currently playing, change the icon to 'pause'; 
        otherwise, change the icon to 'play'.
        """
        
        if self.video_player.state() == QMediaPlayer.PlayingState:
            self.button_play.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.button_play.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        """ Slot function:
        Change the position of the slider.
        """
        
        self.video_slider.setValue(position)

    def duration_changed(self, duration):
        """ Slot function:
        If the duration of the video changed, change the range of the slider.
        This slot function is called after opening a video.
        """
        
        self.video_slider.setRange(0, duration)
        self.video_duration = duration
        self.record_start_time = 0
        self.record_end_time = 0

    def set_position(self, position):
        """ Slot function:
        Change the progress of the video.
        """
        
        self.video_player.setPosition(position)

    def error_control(self):
        """ Slot function:
        If an error occurs while opening the video, this slot function is 
        called.
        """
        
        self.button_play.setEnabled(False)
        self.statusbar.showMessage(
                "Error: An error occurs while opening the video.")

    def record_start(self):
        self.record_start_time = self.video_slider.sliderPosition()
        if self.record_end_time is not None and self.record_end_time != 0 and self.record_start_time > self.record_end_time:
            self.record_start_time, self.record_end_time = self.record_end_time, self.record_start_time

        self._show_record_time()

    def record_end(self):
        self.record_end_time = self.video_slider.sliderPosition()
        if self.record_start_time is not None and self.record_start_time > self.record_end_time:
            self.record_start_time, self.record_end_time = self.record_end_time, self.record_start_time

        self._show_record_time()

    def _show_record_time(self):
        if self.record_start_time is not None and self.record_end_time is not None:
            self.statusbar.showMessage(
                "Info: Starting time: ({}), and Ending time: ({}) (Duration: {}).".format(
                self.record_start_time / 1000, self.record_end_time / 1000, self.video_duration / 1000))

    def _check_duration(self):
        if self.video_name == "":
            self.statusbar.showMessage(
                "Error: Please open a video first.")
        elif self.record_start_time == self.record_end_time: 
            self.statusbar.showMessage(
                "Error: Duration can NOT be 0.")
        elif self.record_start_time > self.record_end_time: 
            self.statusbar.showMessage(
                "Error: The start time should be earlier than the end time.")
        else:
            return True

        return False

    def record_subclip_video(self):
        if self._check_duration():
            # self.video_player.pause()
            self.statusbar.showMessage(
                "Info: Please wait until the process ends.")
            self.thread = Thread()
            self.thread.set_params(Thread.MSG_CUT_VIDEO, self.video_name, 
                self.record_start_time / 1000, self.record_end_time / 1000, self.combobox_degree.currentText())
            self.thread.signal_return_value.connect(self.thread_done)
            self.thread.start()
    
    def record_subclip_audio(self):
        if self._check_duration():
            # self.video_player.pause()
            self.statusbar.showMessage(
                "Info: Please wait until the process ends.")
            self.thread = Thread()
            self.thread.set_params(Thread.MSG_EXTRACT_AUDIO, self.video_name, 
                self.record_start_time / 1000, self.record_end_time / 1000)
            self.thread.signal_return_value.connect(self.thread_done)
            self.thread.start()

    def record_clear(self):
        self.record_start_time = 0
        self.record_end_time = 0

        self.statusbar.showMessage(
                "Info: Starting time: ({}), and Ending time: ({}).".format(self.record_start_time, self.record_end_time))

    def thread_done(self, return_value, video_name):
        if return_value:
            self.statusbar.showMessage(
                "Info: The process has done and saved as {}.".format(video_name))

if __name__ == '__main__':
    """
    app = QApplication(sys.argv) will go wrong.
    """
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
        
    player = VideoWindow()
    player.show()
    
    """
    sys.exit(app.exec_()) will go wrong.
    """
    app.exec_()
    