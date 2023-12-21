import os
import torch
from speech_decoding.decode_text_from_audio import predict
from pathlib import Path

def process_audio_files():
    IN_FILES_DIR = "D:\\Projects\\Karaoke-AI-New\\wav\\"
    SRT_FILES_DIR = "D:\\Projects\\Karaoke-AI-New\\srt\\"

    for filename in os.scandir(IN_FILES_DIR):
        if filename.is_file():
            print("Decoding " + os.path.basename(filename) + "...")

            device = torch.device("cpu")
            model = torch.load("result.model").to(device)
            text = predict(model, filename.path, device)

            print(text)

            srt_file = SRT_FILES_DIR + Path(filename).stem + ".srt"

            with open(srt_file) as f:
                lines = f.readlines()
            lines += ''.join(text) + "\r\n"
            with open(srt_file, "w") as f:
                f.writelines(lines)
