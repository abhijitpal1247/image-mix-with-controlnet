from clip_interrogator import Config, Interrogator
from diffusers.utils import load_image


def generate_captions(image_path):
    caption_model_name = 'blip-large'
    clip_model_name = 'ViT-L-14/openai'
    image = load_image(image_path)
    config = Config()
    config.clip_model_name = clip_model_name
    config.caption_model_name = caption_model_name
    ci = Interrogator(config)
    prompt = ci.interrogate(image)
    return prompt
