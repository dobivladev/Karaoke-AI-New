import torch
import torchaudio
from speech_decoding.greedy_decoder import GreedyCTCDecoder


def decode_using_trained_model(speech_file):
    # device config
    torch.random.manual_seed(7)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # get the pretrained model
    bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
    print("Sample Rate:", bundle.sample_rate)
    print("Labels:", bundle.get_labels())

    # get the model and convert to device format
    model = bundle.get_model().to(device)
    print(model.__class__)

    waveform, sample_rate = torchaudio.load(speech_file)
    waveform = waveform.to(device)

    if sample_rate != bundle.sample_rate:
        waveform = torchaudio.functional.resample(waveform, sample_rate, bundle.sample_rate)

    with torch.inference_mode():
        emission, _ = model(waveform)

    decoder = GreedyCTCDecoder(bundle.get_labels())
    transcript = decoder(emission[0]).replace('|', ' ')

    print(transcript)
    return transcript