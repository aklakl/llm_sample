# The code with autogen testing google gemini api via ngrok mapping litellm service in google colab

* google gemini () refer:https://microsoft.github.io/autogen/docs/Installation
autogen_using_palm_api Resource=>https://youtu.be/J2DYaP6VWVQ?t=57
Google Gemini API=>https://cloud.google.com/vertex-ai/docs/generative-ai/multimodal/send-chat-prompts-gemini

### Running Locally

1. Go to Google colab Start the ngrok mapping litellm server and => https://colab.research.google.com/drive/1NutSWRS4UR38vasK_Y3MTW1Z0AzIOFmE?usp=sharing

  
2. Run your code local machine:

```
python3.11 -m venv pyautogen
source pyautogen/bin/activate
# deactivate
pip install pyautogen google-generativeai
pip install -q google-generativeai

python autogen/autogen-gemini/autogen-gemini.py


```



