# The code with autogen testing multiagents_groupchat


### Running Locally

1. Go to Google colab Start the ngrok mapping litellm server first refer => https://colab.research.google.com/drive/1GKlfU7Fjq30oQPirHvCcQy_e_B8vNEDs?usp=sharing    
Or use LM Studio build your local LLM => https://lmstudio.ai/


2. Run your code local machine:
```
python3.12 -m venv ag2
source ag2/bin/activate
# deactivate
# old version with between Aug 2023 and Oct 2023
pip install openai==0.28  ag2==0.1.14  
# latest 
pip install openai==1.6.1 ag2==0.2.3 
pip show ag2

python autogen/multiagents_groupchat/multiagents_groupchat.py

```



