import os
import torch
from speech_decoding.decode_text_from_audio import predict
from speech_decoding.decode_text_from_audio_trained import decode_using_trained_model
from pathlib import Path

def process_audio_files(model_file, wav_dir, srt_dir):
    for filename in os.scandir(wav_dir):
        if filename.is_file():
            print("Decoding " + os.path.basename(filename) + "...")
            srt_file = srt_dir + Path(filename).stem + ".srt"
            if os.stat(filename).st_size <= 1024:
                print("Skipping due to small size...")
                write_to_srt(srt_file, "")
                continue

            if model_file != '':
                device = torch.device("cpu")
                model = torch.load(model_file).to(device)
                text = predict(model, filename.path, device)
            else:
                text = decode_using_trained_model(filename.path)

            print(text)
            write_to_srt(srt_file, text)

def write_to_srt(srt_file, text):
    with open(srt_file) as f:
        lines = f.readlines()
    lines += ''.join(text) + "\n\n"
    with open(srt_file, "w") as f:
        f.writelines(lines)