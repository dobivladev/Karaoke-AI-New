import shlex
import subprocess
import os

if os.path.exists("output.mp4"):
    os.remove('output.mp4')
command = shlex.split('ffmpeg -loop 1 -framerate 1 -i image.png -i m.wav -map 0:v -map 1:a -r 10 -movflags +faststart -shortest -fflags +shortest -max_interleave_delta 100M output.mp4')
subprocess.run(command)
if os.path.exists("output_srt.mp4"):
    os.remove('output_srt.mp4')
command = shlex.split('ffmpeg -i output.mp4 -filter_complex "subtitles=speech.srt" output_srt.mp4')
subprocess.run(command)