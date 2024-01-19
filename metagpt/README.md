# The code with MetaGPT
```
MetaGPT github => https://github.com/geekan/MetaGPT
MetaGPT Paper => https://arxiv.org/abs/2308.00352
MetaGPT Installation =>https://docs.deepwisdom.ai/main/en/guide/get_started/installation.html#install-stable-version
My Colab => https://colab.research.google.com/drive/1T-JFG_NXSK9cyPrYTFp1t1lXt681aQw8

```

### Running Locally

1. Go to Google colab Start the ngrok mapping litellm server first refer => https://colab.research.google.com/drive/1-pUeLBWvsh0M82OhaXivZigVhtJKhPm_
Or use LM Studio build your local LLM => https://lmstudio.ai/


2. Run your code local machine:
```
export OPENAI_API_KEY=sk-1111111111111111111
export OPENAI_API_BASE=http://airedale-native-chicken.ngrok-free.app/v1

pip install -r requirements.txt --use-deprecated=legacy-resolver

python3.12 -m venv metagptenv
source metagptenv/bin/activate
# deactivate

python llm_sample/ming/metagptenv/



```
