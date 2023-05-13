import torch
from diffusers.utils import load_image
from controlnet_aux import PidiNetDetector, HEDdetector
from PIL import Image
from diffusers import (
    ControlNetModel,
    StableDiffusionControlNetPipeline,
    UniPCMultistepScheduler,
)


def generate_stylized_image(prompt, image_bytes):
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
    pipe.enable_model_cpu_offload()

    generator = torch.manual_seed(0)
    out_image = pipe(prompt, num_inference_steps=30, generator=generator, image=image).images[0]
    return out_image