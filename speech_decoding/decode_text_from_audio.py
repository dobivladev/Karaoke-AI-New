import torch
import torch.nn as nn
import torchaudio
import numpy as np
import librosa
from text_processing.processing import text_transform


def predict(model, file_name, device):
    model.eval()

    # transform the audio into a readable format for the model
    audio_transforms = nn.Sequential(
        torchaudio.transforms.MelSpectrogram(sample_rate=22050, n_mels=128),
        torchaudio.transforms.FrequencyMasking(freq_mask_param=15),
        torchaudio.transforms.TimeMasking(time_mask_param=35)
    )
    audio_transforms = torchaudio.transforms.MelSpectrogram()

    # use librosa to mono and resample the loaded file before transformations
    sampl = librosa.load(file_name, sr=22050)[0]
    sampl = librosa.to_mono(sampl)
    sampl = sampl[np.newaxis, :]
    sampl = torch.Tensor(sampl)
    spectrogram_tensor = audio_transforms(sampl).unsqueeze(0)

    with torch.no_grad():
        spectrogram_tensor.to(device)
        output = model(spectrogram_tensor)
        
        arg_maxes = torch.argmax(output, dim=2)
        decodes = []
        for _, args in enumerate(arg_maxes):
            decode = []
            for j, index in enumerate(args):
                if index != 28 and not (j != 0 and index == args[j -1]):
                    decode.append(index.item())
            decodes.append(text_transform.int_to_text(decode))

    print(decodes)
    return decodes[0]