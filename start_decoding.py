from audio_processing.audio_preparation import AudioAnalisys
from audio_processing.audio_preparation import construct_subtitles
from util.process_wavs_to_text import process_audio_files

# from translation.translation import translate
# from models_enum import Models

WAV_PATH = "D:\\Projects\\Karaoke-AI-New\\wav\\"
SRT_PATH = "D:\\Projects\\Karaoke-AI-New\\srt\\"

filename_video = 'D:\\Projects\\Karaoke-AI-New\\speech.mp4'

# Instantiate the AudioAnalisys class
aa = AudioAnalisys(filename_video, WAV_PATH, SRT_PATH)

# Chunk the audio and generate subtitles
aa.chunk_audio()

process_audio_files()

construct_subtitles(filename_video, SRT_PATH)