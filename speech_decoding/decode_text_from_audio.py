import torch
import torch.utils.data as data
import torch.nn.functional as F
import torchaudio
import numpy as np
import librosa
from speech_decoding.processing import text_transform

def predict(model, file_name, device):
    model.eval()
    valid_audio_transforms = torchaudio.transforms.MFCC(n_mfcc=128)
    
    sampl = librosa.load(file_name, sr=22050)[0]
    sampl = sampl[np.newaxis, :]
    sampl = torch.Tensor(sampl)
    spectr = valid_audio_transforms(sampl).squeeze(0)
    spectrogram_tensor = spectr.unsqueeze(0).unsqueeze(0)
    
    with torch.no_grad():
        spectrogram_tensor.to(device)
        output = model(spectrogram_tensor)
        
        arg_maxes = torch.argmax(output, dim=2)
        decodes = []
        for i, args in enumerate(arg_maxes):
            decode = []
            for j, index in enumerate(args):
                if index != 28:
                    if True and j != 0 and index == args[j -1]:
                        continue
                    decode.append(index.item())
            decodes.append(text_transform.int_to_text(decode))

    return decodes[0]