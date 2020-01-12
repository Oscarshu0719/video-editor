# -*- coding: utf-8 -*-
"""
@author: GitHub@Oscarshu0719
"""

from PyQt5.QtCore import QThread, pyqtSignal
from src.video_cutter import cut_video

class Thread(QThread):
    signal_return_value = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super(Thread, self).__init__()
 
    def __del__(self):
        self.wait() 

    def set_params(self, video_name, start_time, end_time):
        self.video_name = video_name
        self.start_time = start_time
        self.end_time = end_time

    def run(self):
        cut_video_name = cut_video(self.video_name, self.start_time, self.end_time)
        self.signal_return_value.emit(1, cut_video_name)
