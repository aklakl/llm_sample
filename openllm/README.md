# Sample to use openLLM
Docs refer:https://pypi.org/project/openllm/
Offical github=>https://github.com/bentoml/OpenLLM


## openllm Python style
### create local env for python
1. Install python first
```
python3.11 -m venv openllm
source openllm/bin/activate

#Start the openllm service
!nohup openllm start TinyLlama/TinyLlama-1.1B-Chat-v1.0 --port 8001 --dtype float16 --backend vllm > openllm.log 2>&1 &
openllm start microsoft/phi-2 --port 8001 --dtype float16 


#check openllm models
openllm models
bentoml models list

```

## Other version of openllm

### XXX

### Notes


