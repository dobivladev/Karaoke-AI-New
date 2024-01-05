import shlex
import subprocess
import os
from audio_processing.audio_analysis import AudioAnalysis
from util.utils import construct_subtitles
from speech_decoding.process_wavs_to_text import process_audio_files

# Terminal colors
OKGREEN = '\033[92m'
OKPURPLE = '\033[95m'
ENDC = '\033[0m'

WAV_FOLDER_PATH = "wav/"
SRT_FOLDER_PATH = "srt/"

# Change only these
SONG_NAME = 'k'
VOCAL_WAV_NAME = 'vocals'
BACKGROUND_IMG_PATH = 'image.png'
MODEL_PATH = ''

SONG_PATH = SONG_NAME + '.wav'
# Change this to use different audio in the final clip
FINAL_AUDIO_PATH = SONG_PATH
# These are generated after the WAV is decoded and is ready to be assembled
VOCAL_PATH = VOCAL_WAV_NAME + '.wav'
VOCAL_PATH_OUT = VOCAL_WAV_NAME + '.mp4'
VOCAL_SRT_PATH = VOCAL_WAV_NAME + '.srt'
# This is the final file
FINAL_MP4 = SONG_NAME + '_srt.mp4'

# Use spleeter to extract the vocals
print(OKPURPLE + '\nExtracting vocals using spleeter...\n' + ENDC)
command = shlex.split('spleeter separate -p spleeter:2stems -o . {}'.format(SONG_PATH))
subprocess.run(command)
if os.path.exists(VOCAL_PATH):
    os.remove(VOCAL_PATH)
os.replace('{}/vocals.wav'.format(SONG_NAME), VOCAL_PATH)

print(OKPURPLE + '\nSplitting audio into chunks and generating SRT templates...\n' + ENDC)
# Instantiate the AudioAnalisys class
aa = AudioAnalysis(VOCAL_PATH, WAV_FOLDER_PATH, SRT_FOLDER_PATH)
# Chunk the audio and generate subtitle templates
aa.chunk_audio()

print(OKPURPLE + '\nProcessing audio chunks and writing to SRTs...\n' + ENDC)
# Process the vocals and fill the SRTs
process_audio_files(MODEL_PATH, WAV_FOLDER_PATH, SRT_FOLDER_PATH)

print(OKPURPLE + '\nCombining split SRTs into {}...\n'.format(VOCAL_SRT_PATH) + ENDC)
# Combine the split SRT files into 1
construct_subtitles(VOCAL_PATH, SRT_FOLDER_PATH)

print(OKPURPLE + '\nGenerating mp4 file using a static image ({})...\n'.format(BACKGROUND_IMG_PATH) + ENDC)
# Combine the SRT and Original WAV (before spleeter)
if os.path.exists(VOCAL_PATH_OUT):
    os.remove(VOCAL_PATH_OUT)
command = shlex.split('ffmpeg -loop 1 -framerate 1 -i {} -i {} -map 0:v -map 1:a -r 10 -movflags +faststart -shortest -fflags +shortest -max_interleave_delta 100M {}'
                      .format(BACKGROUND_IMG_PATH, FINAL_AUDIO_PATH, VOCAL_PATH_OUT))
subprocess.run(command)
print(OKPURPLE + '\nCombining mp4 file {} and SRT file {} into {}...\n'.format(VOCAL_PATH_OUT, VOCAL_SRT_PATH, FINAL_MP4) + ENDC)
if os.path.exists(FINAL_MP4):
    os.remove(FINAL_MP4)
command = shlex.split('ffmpeg -i {} -filter_complex "subtitles={}" {}'
                      .format(VOCAL_PATH_OUT, VOCAL_SRT_PATH, FINAL_MP4))
subprocess.run(command)

print(OKGREEN + '\nYour file {} is ready!'.format(FINAL_MP4) + ENDC)
