import torch
from clip_interrogator import Config, Interrogator
from PIL import Image
from src.utils.clear_memory import flush


def generate_captions(image_bytes):
    caption_model_name = 'blip-large'
    clip_model_name = 'ViT-L-14/openai'
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    image = Image.open(image_bytes)
    config = Config(device=device)
    config.clip_model_name = clip_model_name
    config.caption_model_name = caption_model_name
    ci = Interrogator(config)
    prompt = ci.interrogate(image)
    del config
    del ci
    flush()
    return prompt
