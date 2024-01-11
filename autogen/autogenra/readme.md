# The code with autogenra
```
autogenra pip instruction refer:https://pypi.org/project/autogenra/
Video instruction =>https://youtu.be/lIqx3zBy58M
```

### Running Locally

1. Go to Google colab Start the ngrok mapping litellm server first refer => https://colab.research.google.com/drive/1GKlfU7Fjq30oQPirHvCcQy_e_B8vNEDs?usp=sharing    
Or use LM Studio build your local LLM => https://lmstudio.ai/


2. Run your code local machine:
```
python3.12 -m venv pyautogen
source pyautogen/bin/activate
# deactivate
# old version with between Aug 2023 and Oct 2023
pip install openai==0.28  pyautogen==0.1.14  
# latest 
pip install openai==1.6.1 pyautogen==0.2.3 

pip install -r requirements.txt


#export your local OPENAI_API_KEY,OPENAI_API_BASE/OPENLLM_ENDPOINT refer:https://github.com/gpt-engineer-org/gpt-engineer/issues/331#issuecomment-1614240500
export OPENAI_API_KEY=sk-1111111111111111111
export OPENAI_API_BASE=http://192.168.0.232:1234/v1

autogenra ui --port 8081


```



