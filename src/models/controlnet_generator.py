import torch
from diffusers.utils import load_image
from controlnet_aux import PidiNetDetector, HEDdetector
from PIL import Image
from diffusers import (
    ControlNetModel,
    StableDiffusionControlNetPipeline,
    UniPCMultistepScheduler,
)
from src.utils.clear_memory import flush

def generate_stylized_image(prompt, image_bytes):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    checkpoint = 'lllyasviel/control_v11p_sd15_softedge'
    image = Image.open(image_bytes)

    #processor = HEDdetector.from_pretrained('lllyasviel/Annotators')
    processor = PidiNetDetector.from_pretrained('lllyasviel/Annotators')
    image = processor(image, safe=True)

    controlnet = ControlNetModel.from_pretrained(checkpoint, torch_dtype=torch.float16)
    pipe = StableDiffusionControlNetPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", controlnet=controlnet, torch_dtype=torch.float16
    )

    pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
    pipe.to(device)

    generator = torch.manual_seed(0)
    out_image = pipe(prompt, num_inference_steps=50, generator=generator, image=image).images[0]
    del processor
    del controlnet
    del pipe
    del generator
    flush()
    return out_image
