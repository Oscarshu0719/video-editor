# -*- coding: utf-8 -*-
"""
@author: GitHub@Oscarshu0719
"""

from PyQt5.QtCore import QThread, pyqtSignal
from src.video_cutter import cut_video, extract_audio

class Thread(QThread):
    MSG_CUT_VIDEO = 1
    MSG_EXTRACT_AUDIO = 2

    signal_return_value = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super(Thread, self).__init__()
 
    def __del__(self):
        self.wait() 

    def set_params(self, msg, video_name, start_time, end_time):
        self.msg = msg
        self.video_name = video_name
        self.start_time = start_time
        self.end_time = end_time

    def run(self):
        if self.msg == Thread.MSG_CUT_VIDEO:
            subclip_name = cut_video(self.video_name, self.start_time, self.end_time)
        elif self.msg == Thread.MSG_EXTRACT_AUDIO:
            subclip_name = extract_audio(self.video_name, self.start_time, self.end_time)

        self.signal_return_value.emit(1, subclip_name)
