# -*- coding: utf-8 -*-
"""
@author: GitHub@Oscarshu0719
"""

from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.rotate import rotate

def cut_video(video_name, start_time=0, end_time=None):
    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration
        
    clip = clip.subclip(start_time, end_time)
    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '_{}_{}'.format(start_time, end_time) + video_name[dot_index: ]
    clip.write_videofile(cut_video_name)

    return cut_video_name

def extract_audio(video_name, start_time=0, end_time=None):
    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration
        
    clip = clip.subclip(start_time, end_time)
    dot_index = video_name.rfind('.')
    cut_audio_name = video_name[: dot_index] + '_audio_{}_{}.mp3'.format(start_time, end_time)
    clip.audio.write_audiofile(cut_audio_name)

    return cut_audio_name

def rotate_video(video_name, start_time=0, end_time=None, degree=0):
    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration

    clip = rotate(clip.subclip(start_time, end_time), degree)

    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '_{}_{}'.format(start_time, end_time) + video_name[dot_index: ]
    clip.write_videofile(cut_video_name)

    return cut_video_name
