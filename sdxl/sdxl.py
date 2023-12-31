
'''
#refer:https://huggingface.co/docs/diffusers/using-diffusers/sdxl_turbo
Simple SDXL(Stable Diffusion XL) with colab notebook=>https://colab.research.google.com/drive/1_7hTIKkIKJOkGqIevOTX5L8cViayBNR9
refer：https://huggingface.co/stabilityai/sdxl-turbo/discussions/20 

python3.11 -m venv sdxl
source sdxl/bin/activate
# deactivate
#pip install -q diffusers transformers accelerate omegaconf
pip install -r requirements.txt

'''
from diffusers import AutoPipelineForText2Image
from diffusers import AutoPipelineForImage2Image
from diffusers.utils import load_image, make_image_grid

import torch
gpu = torch.cuda.is_available()
opt_usage = f"{'GPU' if gpu else 'CPU'}usage"
print(opt_usage)

def run_sdxl_turbo_pipeline_text2image():
    try:
        #device = torch.device("cpu")
        if gpu==True:
            #This is for cuda GPU
            pipeline_text2image = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16").to("cuda")
        else:
            #This is for cpu
            pipeline_text2image = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo")

        #prompt = "A cinematic shot of a baby racoon wearing an intricate italian priest robe."
        prompt = "cute dogs"
        prompt = "cat wizard, gandalf, lord of the rings, detailed, fantasy, cute, adorable, Pixar, Disney, 8k, with happy birthday word"
        prompt = "cute cat Abyssinian, stand on the globe"


        image = pipeline_text2image(prompt=prompt, guidance_scale=0.0, num_inference_steps=1).images[0]
        #print(image)
        # save a image using extension  refer:https://www.geeksforgeeks.org/python-pil-image-save-method/
        res_image = image.save("./images/Abyssinian stand on the globe.jpg") 
        print("==========Completed pipeline_text2image==============")
    except Exception as e:
        print(
            f"""run_sdxl_turbo_pipeline_text2image failed with Exception{e}. \n"""
        ) 

def run_sdxl_turbo_pipeline_image2image():
    # try:
        # use from_pipe to avoid consuming additional memory when loading a checkpoint
       
        if gpu==True:
            pipeline_text2image = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16").to("cuda")     
            pipeline = AutoPipelineForImage2Image.from_pipe(pipeline_text2image).to("cuda")     
        else:
            pipeline_text2image = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo")
            pipeline = AutoPipelineForImage2Image.from_pipe(pipeline_text2image)
        
        # This image_url is not supporting PIL, that's the base64 formatting   with "data:image/x-icon;base64,"
        # image_url = "https://oss.feidee.net/oss//group_oss_trans3_f9651cb59a6ee921_1597X1276.jpg"
        # This is fitting PIL formatting 
        image_url = "https://s3.amazonaws.com/formaloo-en/f/uploads/ur/89cd8be71d781d86/fm/NriKaD2r/b1339f6c-6e02-4755-a172-9080b8625bdb.jpg"
        init_image = load_image(image_url)
        init_image = init_image.resize((1597, 1276))
        #prompt = "Enhance the cuteness of this portrait, please."
        prompt = "Chage the backgroup with outdoor,won't be change portrait"
        prompt = ""
        image = pipeline(prompt, image=init_image, strength=0.5, guidance_scale=0.0, num_inference_steps=2).images[0]
        print(image)
        #image.images[0]
        make_image_grid([init_image, image], rows=1, cols=2)
        res_image = image.save("./images/image2image4.jpg") 
        print("==========Completed run_sdxl_turbo_pipeline_image2image==============")
    # except Exception as e:
    #     print(f"""run_sdxl_turbo_pipeline_image2image failed with Exception{e}. \n""")    

def run_sdxl_turbo_googletrans_text2image():
    if gpu==True:
        #This is for cuda GPU
        pipeline_text2image = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16").to("cuda")
    else:
        #This is for cpu
        pipeline_text2image = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo")
    # @title Generation
    Prompt = "cute dogs" # @param {type:"string"}
    Steps = 1 # @param {type:"number"}

    from googletrans import Translator, constants
    from pprint import pprint
    translator = Translator()
    translation = translator.translate(Prompt)
    PromptEN = translation.text
    prompt = PromptEN
    if gpu==False:
        image = pipeline_text2image(prompt=PromptEN, num_inference_steps=1, guidance_scale=0.0).images[0]
    else:
        image = pipeline_text2image(prompt=PromptEN, num_inference_steps=Steps, guidance_scale=0.0).images[0]
    res_image = image.save("./images/image2image.jpg") 
    print("==========Completed run_sdxl_turbo_googletrans_text2image ==============")

#running
if __name__ == "__main__":
    #run_sdxl_turbo_pipeline_text2image()
    run_sdxl_turbo_pipeline_image2image()