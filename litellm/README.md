# The code with litellm 

```

litellm offical Website => https://github.com/BerriAI/litellm
litellm docs => https://docs.litellm.ai/
litellm pip => https://pypi.org/project/litellm/



```

### Install litellm

Suppose you don't have sudo permissions. you can install Ollama with source code as well. Please refer:https://github.com/jmorganca/ollama?tab=readme-ov-file#building

```
pip install litellm

#configuration => https://docs.litellm.ai/docs/proxy/configs
#litellm --config /path/to/config.yaml

litellm --config /scratch/network/sl6723/repo/llm_sample/litellm/config/config.yaml
litellm --model ollama/phi
litellm --test


```



### Running Locally 

1. Go to Google colab Start the ngrok mapping litellm server first refer => https://colab.research.google.com/drive/1-pUeLBWvsh0M82OhaXivZigVhtJKhPm_   
Or use LM Studio build your local LLM => https://lmstudio.ai/


2. Run your code local machine:
```
export OPENAI_API_KEY=sk-1111111111111111111
export OPENAI_API_BASE=http://airedale-native-chicken.ngrok-free.app/v1
#export OPENAI_API_BASE=http://192.168.0.232:1234/v1


python3.12 -m venv ollamademoenv
source ollamademoenv/bin/activate
# deactivate

python llm_sample/ollamademo/ollamademo.py

```



## Customize a model => Import from GGUF=>https://github.com/jmorganca/ollama?tab=readme-ov-file#import-from-gguf
### Import from GGUF  

Ollama supports importing GGUF models in the Modelfile:
GGUF (GPT-Generated Unified Format), introduced as a successor to GGML (GPT-Generated Model Language), was released on the 21st of August, 2023. This format represents a significant step forward in the field of language model file formats, facilitating enhanced storage and processing of large language models like GPT. refer:https://medium.com/@phillipgimmi/what-is-gguf-and-ggml-e364834d241c


1.download your gguf model to local disk first. You can get from https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard


2. Create a file named `Modelfile`, with a `FROM` instruction with the local filepath to the model you want to import.(Replace the model name in `Modelfile` and save the `Modelfile`)
If you have bin file,  please refer:https://github.com/jmorganca/ollama/blob/main/docs/import.md
   ```

   FROM ./vicuna-33b.Q4_0.gguf

   ```

3. Create the model in Ollama

   ```
   ollama create example -f Modelfile
   ```

4. Check you just created the model

   ```

   ollama list

   ```

5. Run the model

   ```

   ollama run example

   ```
   

