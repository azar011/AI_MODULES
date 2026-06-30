from transformers import AutoProcessor, SeamlessM4Tv2Model
import torchaudio
import torch

MODEL_NAME = "facebook/seamless-m4t-v2-large"

device = "cuda" if torch.cuda.is_available() else "cpu"

processor = AutoProcessor.from_pretrained(MODEL_NAME)
model = SeamlessM4Tv2Model.from_pretrained(MODEL_NAME).to(device)

def translate_audio(audio_path):

    waveform, sample_rate = torchaudio.load(audio_path)

    if sample_rate != 16000:
        waveform = torchaudio.transforms.Resample(
            sample_rate,
            16000
        )(waveform)

    audio = waveform.squeeze().numpy()

    inputs = processor(
        audios=audio,
        sampling_rate=16000,
        return_tensors="pt"
    ).to(device)

    output = model.generate(
        **inputs,
        tgt_lang="eng"
    )

    text = processor.decode(
        output[0],
        skip_special_tokens=True
    )

    return text