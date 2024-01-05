import librosa
import numpy as np
import pydub
import os


def construct_subtitles(file, srt_path):
    filename = get_name(file) + '.srt'
    file_write = open(filename, 'w')
    print("Constructing subtitles...")
    for file in os.listdir(srt_path):
        with open(srt_path + file) as file_read:
            for line in file_read.readlines():
                file_write.write(line)
    file_write.close()


def format_timestamp(milliseconds, always_include_hours = True):
    # creates srt timestamps
    seconds = milliseconds // 1000
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
    return f"{hours_marker}{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def get_name(filename):
    # Gets the name of a file without the extension

    return filename.split('.')[0]


def create_emty_directory(dir_name):
    # Creates an empty directory
    # If a directory with the same name exists, deletes its content

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    else:
        for x in os.listdir(dir_name):
            os.remove(os.path.join(dir_name, x))


def write_to_srt(srt_file, text):
    # writes text to a specified srt file
    with open(srt_file) as f:
        lines = f.readlines()
    lines += ''.join(text) + "\n\n"
    with open(srt_file, "w") as f:
        f.writelines(lines)