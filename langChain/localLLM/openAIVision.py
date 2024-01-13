
# Adapted from OpenAI's Vision example 
from openai import OpenAI
import base64
import requests
import os

from langchain.llms import OpenLLM
# Do this so we can see exactly what's going on under the hood
from langchain.globals import set_debug
from langchain.globals import set_verbose
from getpass import getpass

#for debuging refer:https://python.langchain.com/docs/guides/debugging
set_debug(True)
set_verbose(True)
print("==============================================Completed the setup env=========================")
#==============================================Completed the setup env=========================




#==============================================exact logic code with openAI version higher 1.0.0=========================
#Initialize LLM language model
base_url = os.environ.get("TEST_API_BASE_URL", "http://192.168.0.232:1234")     # 1234  3000
api_key = os.environ.get("OPENAI_API_KEY", "xxxxxxxxx")   # even your local don't use the authorization, but you need to fill something, otherwise will be get exception.
api_key = "xxxx"


def run_openai_vision():
    # Point to the local server
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

    # Ask the user for a path on the filesystem:
    path = input("Enter a local filepath to an image: ")

    # Read the image and encode it to base64:
    base64_image = ""
    try:
      image = open(path.replace("'", ""), "rb").read()
      base64_image = base64.b64encode(image).decode("utf-8")
    except:
      print("Couldn't read the image. Make sure the path is correct and the file exists.")
      exit()

    completion = client.chat.completions.create(
      model="local-model", # not used
      messages=[
        {
          "role": "system",
          "content": "This is a chat between a user and an assistant. The assistant is helping the user to describe an image.",
        },
        {
          "role": "user",
          "content": [
            {"type": "text", "text": "What’s in this image?"},
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              },
            },
          ],
        }
      ],
      max_tokens=1000,
      stream=True
    )

    for chunk in completion:
      if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)





#running main method
if __name__ == "__main__":
    #run_openai_completion()
    run_openai_vision()

