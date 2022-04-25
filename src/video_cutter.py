# -*- coding: utf-8 -*-
"""
@author: GitHub@Oscarshu0719
"""

import subprocess

def run(cmd):
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        encoding='utf-8',
        errors='replace'
    )

    while True:
        realtime_output = process.stdout.readline()

        if realtime_output == '' and process.poll() is not None:
            break

        if realtime_output:
            print(realtime_output.strip(), flush=True)

    return process

def get_video_stream(path):
    try:
        result = subprocess.run(f'ffprobe -i "{path}" -show_entries format=duration -v quiet -of csv="p=0"', 
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8", timeout=1)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return 0
    except Exception as err:
        print(str(err.stderr, encoding='utf8'))
        return 0

def cut_video(video_name, start_time=0, end_time=None):
    if not end_time:
        end_time = get_video_stream(video_name)

    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '_{}_{}'.format(start_time, end_time) + video_name[dot_index: ]

    run(f'ffmpeg -i "{video_name}" -ss {start_time} -t {end_time - start_time} "{cut_video_name}"')

    return cut_video_name

def extract_audio(video_name, start_time=0, end_time=None):
    if not end_time:
        end_time = get_video_stream(video_name)

    dot_index = video_name.rfind('.')
    cut_audio_name = video_name[: dot_index] + '_{}_{}'.format(start_time, end_time) + '.mp3'

    run(f'ffmpeg -i "{video_name}" -ss {start_time} -t {end_time - start_time} -q:a 0 -map a "{cut_audio_name}"')

    return cut_audio_name

def rotate_video(video_name, start_time=0, end_time=None, degree=0):
    if not end_time:
        end_time = get_video_stream(video_name)

    """
        Rotation (clockwise):
            90: transpose=0
            180: transpose=2,transpose=2
            270: transpose=2
    """
    transpose_dict = {
        '90': 'transpose=0',
        '180': 'transpose=2,transpose=2', 
        '270': 'transpose=2'
    }
    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '_{}_{}'.format(start_time, end_time) + video_name[dot_index: ]

    traspose_method = transpose_dict[str(degree)]
    run(f'ffmpeg -i "{video_name}" -ss {start_time} -t {end_time - start_time} -vf "{traspose_method}" "{cut_video_name}"')

    return cut_video_name
