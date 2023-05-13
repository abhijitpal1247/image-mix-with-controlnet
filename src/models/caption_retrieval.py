from clip_interrogator import Config, Interrogator
from PIL import Image


def generate_captions(image_bytes):
    caption_model_name = 'blip-large'
    clip_model_name = 'ViT-L-14/openai'
    image = Image.open(image_bytes)
    config = Config()
    config.clip_model_name = clip_model_name
    config.caption_model_name = caption_model_name
    ci = Interrogator(config)
    prompt = ci.interrogate(image)
    return prompt
