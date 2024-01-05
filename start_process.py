import shlex
import subprocess
import os
from audio_processing.audio_analysis import AudioAnalysis
from util.utils import construct_subtitles
from speech_decoding.audio_decoding_to_srt import process_audio_to_srt

# Terminal colors
OKGREEN = '\033[92m'
OKPURPLE = '\033[95m'
ENDC = '\033[0m'

# Audio and SRT chunk folders
WAV_FOLDER_PATH = "wav/"
SRT_FOLDER_PATH = "srt/"

# Change only these
SONG_NAME = 'k' # Song name without the extension
VOCAL_WAV_NAME = 'vocals' # The name of the file that we get from spleeter without the extension
BACKGROUND_IMG_PATH = 'image.png'
MODEL_PATH = 'result.model.4'

# Do not touch these unless necessary
SONG_PATH = SONG_NAME + '.wav'
# Change this to use different audio in the final clip, e.g. we can use the original song above to extract vocals and accompaniment
# then process the vocals, but change the FINAL_AUDIO_PATH to use the accompaniment to create the clip, which creates a karaoke clip
# FINAL_AUDIO_PATH = SONG_NAME + '/accompaniment.wav'
FINAL_AUDIO_PATH = SONG_PATH
# These are generated after the WAV is decoded and is ready to be assembled
VOCAL_PATH = VOCAL_WAV_NAME + '.wav'
VOCAL_PATH_OUT = VOCAL_WAV_NAME + '.mp4'
VOCAL_SRT_PATH = VOCAL_WAV_NAME + '.srt'
# This is the final file
FINAL_MP4 = SONG_NAME + '_srt.mp4'

# Use spleeter to extract the vocals
print(f'{OKPURPLE}\nExtracting vocals using spleeter...\n{ENDC}')
command = shlex.split(f'spleeter separate -p spleeter:2stems -o . {SONG_PATH}')
subprocess.run(command)
if os.path.exists(VOCAL_PATH):
    os.remove(VOCAL_PATH)
os.replace(f'{SONG_NAME}/vocals.wav', VOCAL_PATH)

print(f'{OKPURPLE}\nSplitting audio into chunks and generating SRT templates...\n{ENDC}')
# Instantiate the AudioAnalisys class
aa = AudioAnalysis(VOCAL_PATH, WAV_FOLDER_PATH, SRT_FOLDER_PATH)
# Chunk the audio and generate subtitle templates
aa.chunk_audio()

print(f'{OKPURPLE}\nProcessing audio chunks and writing to SRTs...\n{ENDC}')
# Process the vocals and fill the SRTs
process_audio_to_srt(MODEL_PATH, WAV_FOLDER_PATH, SRT_FOLDER_PATH)

print(f'{OKPURPLE}\nCombining split SRTs into {VOCAL_SRT_PATH}...\n{ENDC}')
# Combine the split SRT files into 1
construct_subtitles(VOCAL_PATH, SRT_FOLDER_PATH)

print(f'{OKPURPLE}\nGenerating mp4 file using a static image ({BACKGROUND_IMG_PATH})...\n{ENDC}')
# Combine the SRT and set WAV
if os.path.exists(VOCAL_PATH_OUT):
    os.remove(VOCAL_PATH_OUT)
command = shlex.split(f'''ffmpeg -loop 1 -framerate 1 -i {BACKGROUND_IMG_PATH} -i {FINAL_AUDIO_PATH} -map 0:v -map 1:a 
                      -r 10 -movflags +faststart -shortest -fflags +shortest -max_interleave_delta 100M {VOCAL_PATH_OUT}''')
subprocess.run(command)
print(f'{OKPURPLE}\nCombining mp4 file {VOCAL_PATH_OUT} and SRT file {VOCAL_SRT_PATH} into {FINAL_MP4}...\n{ENDC}')
if os.path.exists(FINAL_MP4):
    os.remove(FINAL_MP4)
command = shlex.split(f'ffmpeg -i {VOCAL_PATH_OUT} -filter_complex "subtitles={VOCAL_SRT_PATH}" {FINAL_MP4}')
subprocess.run(command)

print(f'{OKGREEN}\nYour file {FINAL_MP4} is ready!{ENDC}')
