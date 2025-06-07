import os
import torch
import numpy as np
from PIL import Image
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer
from diffusers import StableDiffusionPipeline, DDIMScheduler
import moviepy.editor as mpy

# ========== CONFIG ==========
QUOTES = [
    "Every accomplishment starts with the decision to try",
    "You are capable of amazing things",
    "Your potential is endless",
    "Small steps lead to big achievements",
    "Believe in your limitless potential",
    "Strength grows in the moments you don't give up",
    "Your attitude determines your direction",
    "Make today so awesome that yesterday gets jealous",
    "Progress, not perfection",
    "You become what you believe"
]
OUTPUT_DIR = "motivational_videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)
torch.manual_seed(42)

# Detect device
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# ========== INITIALIZE MODELS ==========
def init_tts():
    print(f"Initializing TTS on {DEVICE}")
    manager = ModelManager()
    tts_path, tts_config, _ = manager.download_model("tts_models/en/ljspeech/tacotron2-DDC")
    voc_path, voc_config, _ = manager.download_model("vocoder_models/en/ljspeech/hifigan_v2")
    return Synthesizer(
        tts_checkpoint=tts_path,
        tts_config_path=tts_config,
        vocoder_checkpoint=voc_path,
        vocoder_config=voc_config,
        use_cuda=(DEVICE == "cuda")
    )

def init_image_gen():
    print(f"Initializing Stable Diffusion v1.4 on {DEVICE}")
    model_id = "CompVis/stable-diffusion-v1-4"
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        scheduler=DDIMScheduler.from_pretrained(model_id, subfolder="scheduler"),
        safety_checker=None,
        requires_safety_checker=False
    )
    return pipe.to(DEVICE)

# ========== GENERATE COMPONENTS ==========
def generate_audio(tts, text, path):
    print(f"Generating audio for: {text}")
    wav = tts.tts(text)
    tts.save_wav(wav, pATH)

def create_video(img_path, audio_path, video_path):
    # load audio and image
    audio = mpy.AudioFileClip(audio_path)
    duration = audio.duration
    orig = Image.open(img_path).convert("RGB")
    w, h = orig.size

    # frame generator with manual zoom-out
    def make_frame(t):
        zoom = 1.05 - 0.05 * min(t / duration, 1.0)
        nw, nh = int(w * zoom), int(h * zoom)
        resized = orig.resize((nw, nh), resample=Image.Resampling.LANCZOS)
        left, top = (nw - w)//2, (nh - h)//2
        cropped = resized.crop((left, top, left + w, top + h))
        return np.array(cropped)

    # build clip
    clip = mpy.VideoClip(make_frame, duration=duration)
    clip = clip.set_audio(audio).fadein(0.5).fadeout(1.0)
    clip.write_videofile(
        video_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        bitrate="4000k",
        audio_bitrate="192k",
        logger=None
    )
    print(f"Video exported: {video_path}")

# ========== MAIN ==========
def main():
    print("Starting Motivational Video Generator")
    tts = init_tts()
    pipe = init_image_gen()

    for i, quote in enumerate(QUOTES, start=1):
        print(f"[{i}] {quote}")
        base = f"quote_{i}"
        audio_path = os.path.join(OUTPUT_DIR, base + ".wav")
        img_path   = os.path.join(OUTPUT_DIR, base + ".jpg")
        vid_path   = os.path.join(OUTPUT_DIR, base + ".mp4")

        generate_audio(tts, quote, audio_path)
        generate_image(pipe, quote, img_path)
        create_video(img_path, audio_path, vid_path)

    print("All done. Videos saved to:", os.path.abspath(OUTPUT_DIR))

if __name__ == "__main__":
    main()
