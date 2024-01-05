import pydub
from pydub import AudioSegment
from pydub.silence import detect_silence
import numpy as np
import os
import librosa
import soundfile
from util.utils import create_emty_directory, format_timestamp


class AudioAnalysis:
    # Prepares an audio segments from a master file to be estimated

    def __init__(self, audio_file, wav_path, str_path, format = 'wav'):
        self.sound_format = format
        self.str_format = 'srt'
        self.filename = audio_file

        temp = AudioSegment.from_wav(audio_file) # load audio file into an object
        temp = temp.set_frame_rate(22050) # set audio to 22khz
        self.audio = temp

        self.wav_path = wav_path
        self.str_path = str_path
        create_emty_directory(self.wav_path)
        create_emty_directory(self.str_path)

    def generate_srt_file(self, chunk_number, time):
        # Generates a str file template for an audio file

        chunk_name = f'chunk{chunk_number:03}'
        str_file = f'{self.str_path}{chunk_name}.{self.str_format}'
        f = open(str_file, 'w')
        f.write(f'{chunk_number + 1}\n')
        begin = format_timestamp(time[0])
        end = format_timestamp(time[1])
        f.write(f'{begin} --> {end}\n')
        f.close()

    def generate_wav_file(self, chunk_number, time):
        # Extract a part form an audio file (from:to time)

        chunk_name = f'chunk{chunk_number:03}'
        out_file = f'{self.wav_path}{chunk_name}.{self.sound_format}'
        chunk = self.audio[time[0]:time[1]]
        chunk.export(out_file, format=self.sound_format)

        # librosa formats the file so that it is compatible with our model
        audio_data, sample_rate = librosa.load(out_file)
        audio_data = librosa.to_mono(audio_data)
        audio_data = librosa.resample(audio_data, sample_rate, 22050)
        soundfile.write(out_file, audio_data, 22050)

    def chunk_audio(self, min_silence_len_millis=100, silence_thresh_db=-40):
        # Detects the silence parts of an audio file
        # and extracts the different speech parts between the pauses

        # pydub -> detects silences and gives us the timestamps as an array
        silences = detect_silence(self.audio, min_silence_len_millis, silence_thresh_db)

        # find the audio chunks using the silences
        audio_chunks_times = [(0 if i == 0 else silences[i - 1][1], silences[i][0])
                              for i in range(len(silences))]

        # time is an array with a size of 2, that contains the start and end timestamps of the current audio chunk
        for i, time in enumerate(audio_chunks_times):
            self.generate_wav_file(i, time)
            self.generate_srt_file(i, time)
