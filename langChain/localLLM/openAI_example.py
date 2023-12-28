# Example: reuse your existing OpenAI setup (PS: Seem like this based on openAI version is less than 1.0.0[pip install openai==0.28]; This build by LM Studio's python example)
import os
import openai

openai.api_base = "http://192.168.0.232:1234/v1" # point to the local server
openai.api_key = "" # no need for an API key

completion = openai.ChatCompletion.create(
  model="local-model", # this field is currently unused
  messages=[
    {"role": "system", "content": "Always answer in rhymes."},
    {"role": "user", "content": "Introduce yourself."}
  ]
)

print(completion.choices[0].message)


'''
#============================================================
#This is after run "openai migrate" got the modification logic
import os
import openai
from openai import OpenAI

client = OpenAI(api_key="")

# TODO: The 'openai.api_base' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(api_base="http://localhost:1234/v1")'
# openai.api_base = "http://localhost:1234/v1" # point to the local server
 # no need for an API key

completion = client.chat.completions.create(model="local-model", # this field is currently unused
messages=[
  {"role": "system", "content": "Always answer in rhymes."},
  {"role": "user", "content": "Introduce yourself."}
])

print(completion.choices[0].message)
#============================================================
'''