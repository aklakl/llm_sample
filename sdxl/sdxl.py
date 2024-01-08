
'''
#refer:https://huggingface.co/docs/diffusers/using-diffusers/sdxl_turbo
python3.11 -m venv sdxl
source sdxl/bin/activate
# deactivate

pip install -q diffusers transformers accelerate omegaconf
'''
from diffusers import AutoPipelineForText2Image
import torch

#device = torch.device("cpu")
pipeline_text2image = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16")
pipeline_text2image = pipeline_text2image.to("cuda")
#pipeline_text2image = pipeline_text2image.to("cpu")
#device = torch.device("cpu")

prompt = "A cinematic shot of a baby racoon wearing an intricate italian priest robe."

image = pipeline_text2image(prompt=prompt, guidance_scale=0.0, num_inference_steps=1).images[0]
image

print("========================")