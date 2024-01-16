# The code with crewAI
```
crewAI github refer:https://github.com/joaomdmoura/crewAI

```

### Running Locally

1. Go to Google colab Start the ngrok mapping litellm server first refer => https://colab.research.google.com/drive/1GKlfU7Fjq30oQPirHvCcQy_e_B8vNEDs?usp=sharing    
Or use LM Studio build your local LLM => https://lmstudio.ai/


2. Run your code local machine:
```
export OPENAI_API_KEY=sk-1111111111111111111
export OPENAI_API_BASE=http://airedale-native-chicken.ngrok-free.app/v1
#export OPENAI_API_BASE=http://192.168.0.232:1234/v1

pip install -r requirements.txt --use-deprecated=legacy-resolver

python3.12 -m venv crewagent
source crewagent/bin/activate
# deactivate

python llm_sample/mcrewagent/crewagent.py



```



