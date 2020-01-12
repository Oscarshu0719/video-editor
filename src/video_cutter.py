# -*- coding: utf-8 -*-
"""
@author: GitHub@Oscarshu0719
"""

from moviepy.editor import VideoFileClip, concatenate_videoclips

def cut_video(video_name, start_time, end_time):
    clip = VideoFileClip(video_name).subclip(start_time, end_time)
    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '_{}_{}'.format(start_time, end_time) + video_name[dot_index: ]
    clip.write_videofile(cut_video_name)

    return cut_video_name
