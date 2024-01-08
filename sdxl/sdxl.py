
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
#This is for cuda GPU
#pipeline_text2image = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16").to("cuda")

#This is for cpu
pipeline_text2image = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo")



#prompt = "A cinematic shot of a baby racoon wearing an intricate italian priest robe."
prompt = "cute dogs"
prompt = "cat wizard, gandalf, lord of the rings, detailed, fantasy, cute, adorable, Pixar, Disney, 8k, with happy birthday word"
prompt = "cute cat Abyssinian, stand on the globe"


image = pipeline_text2image(prompt=prompt, guidance_scale=0.0, num_inference_steps=1).images[0]
image
#print(image)
# save a image using extension  refer:https://www.geeksforgeeks.org/python-pil-image-save-method/
im1 = image.save("./images/Abyssinian stand on the globe.jpg") 
print("========================")