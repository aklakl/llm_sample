# The code with testing AgentGPT 

AgentGPT=>agentgpt.reworkd.ai
github=>https://github.com/reworkd/AgentGPT
refer:https://youtu.be/6jl0Cux3tUU

### Running Locally

1. Go to Google colab Start the ngrok mapping litellm server first refer => https://colab.research.google.com/drive/1GKlfU7Fjq30oQPirHvCcQy_e_B8vNEDs?usp=sharing    
Or use LM Studio build your local LLM => https://lmstudio.ai/


2. Run your code local machine:
```
python3.12 -m venv autogptenv
source autogptenv/bin/activate
# deactivate
pip install openai==1.6.1 pyautogen==0.2.3 
pip show openai

python autogen/multiagents_groupchat/multiagents_groupchat.py

```



