# Aider is AI pair programming in your terminal
```
Aider  github => https://github.com/paul-gauthier/aider
Ming's Colab within built the LLM for replacing your openai service API =>  https://colab.research.google.com/drive/1-pUeLBWvsh0M82OhaXivZigVhtJKhPm_
Universal Ctags Github => https://github.com/universal-ctags/ctags
Simple video =>https://youtu.be/df8afeb1FY8

```

### Running Locally

1. Go to Google colab Start the ngrok mapping litellm server first refer => https://colab.research.google.com/drive/1-pUeLBWvsh0M82OhaXivZigVhtJKhPm_
Or use LM Studio build your local LLM => https://lmstudio.ai/


2. Run your code local machine:
```
export OPENAI_API_KEY=sk-1111111111111111111
export OPENAI_API_BASE=http://airedale-native-chicken.ngrok-free.app/v1

pip install -r requirements.txt --use-deprecated=legacy-resolver

python3.12 -m venv aiderenv
source aiderenv/bin/activate
# deactivate

python llm_sample/ming/aiderenv/



```
