# Ming's CLI

### Coding Style Guide
In general, we adhere to [Google Python style guide](https://google.github.io/styleguide/pyguide.html).


* Build the free LLM based on free resources or locally 
* Go to Google colab Start the ngrok mapping LiteLLM services => https://drive.google.com/file/d/1IZnVZQJQqLKf_VleM3a5bsfWfKIYfSdE/view?usp=sharing
* Go to Google colab Start the ngrok mapping the TextGen LLM services => https://colab.research.google.com/drive/1-pUeLBWvsh0M82OhaXivZigVhtJKhPm_   
* LM Studio build your local LLM => https://lmstudio.ai/



### Common customized base_url
```
base_url = "http://192.168.40.229:1234/v1"      #Sidan's local Server Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q8_0.gguf
base_url = "http://dashing-slowly-kiwi.ngrok-free.app/v1"      #Sidan's ngrok url 
base_url = "http://airedale-native-chicken.ngrok-free.app/v1"  # Seems like OpenLLM server only support SKD is openai==0.28  


```



### Common customized model
```
Ollama run saikatkumardey/tinyllama   (Ollama model around 903MB) => refer：https://ollama.ai/saikatkumardey/tinyllama 



ALL the Tiny models for testing and simple task (Most model come from Huggingface)[PS: Tiny-Vicuna-1B-GGUF is working as well in colab]
Huggingface Tiny tinyllamas model gguf formating(around 1M refer:https://github.com/ggerganov/llama.cpp/issues/2708) => https://huggingface.co/klosax/tinyllamas-stories-gguf/blob/main/tinyllamas-stories-260k-f32.gguf
LocalDocs text embeddings model Necessary for LocalDocs feature Used for retrieval augmented generation (RAG)[around 40MB] =>https://gpt4all.io/models/gguf/all-MiniLM-L6-v2-f16.gguf
Huggingface =>https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
llama-tiny-Synthetic-therapist-GGUF (adapter_model.safetensors file around 49MB) => https://huggingface.co/wesley7137/llama-tiny-Synthetic-therapist-GGUF
LinguaMatic-Tiny-GGUF (Around 483MB~904MB) => https://huggingface.co/erfanzar/LinguaMatic-Tiny-GGUF
Tiny-Vicuna-1B-GGUF (around 482MB~1.17G) => https://huggingface.co/afrideva/Tiny-Vicuna-1B-GGUF
TinyLlama-1.1B-Chat-v0.3-GGUF(around 482MB~1.17G)  => https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v0.3-GGUF   (Huggingface-API https://huggingface.co/api/models/TheBloke/TinyLlama-1.1B-Chat-v0.3-GGUF/   TinyLlama introduction=>https://youtu.be/T5l228844NI)
TinyLlama-1.1B-1T-OpenOrca-GGUF(around 482MB~1.17G) => https://huggingface.co/TheBloke/TinyLlama-1.1B-1T-OpenOrca-GGUF
Official TinyLlama (ggml-model-q4_0.gguf 637 MB）=> https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v0.2-GGUF
Official code TinyLlama with python (ggml-model-q4_0.gguf 637 MB)=> https://huggingface.co/TinyLlama/TinyLlama-1.1B-python-v0.1
Huggingface tinyllamas  （bin file style around 438 MB） => https://huggingface.co/karpathy/tinyllamas

Huggingface Vision Models (GGUF)=>https://huggingface.co/collections/lmstudio-ai/vision-models-gguf-6577e1ce821f439498ced0c1


More than 4K content token 
Yi-6B-200K content token (2.18 GB~9.94G)=>https://huggingface.co/01-ai/Yi-6B-200K
yi-34b-200k-llamafied.Q2_K.gguf = 14.6 GB (around 14.6 GB~36.5 GB) =>https://huggingface.co/TheBloke/Yi-34B-200K-Llamafied-GGUF
SG-Raccoon-Yi-200k model (around 23GB~45GB)[sg-raccoon-yi-200k-2.0.Q2_K.gguf=21.83 GiB(token content=200k)]=>https://huggingface.co/TheBloke/SG-Raccoon-Yi-200k-2.0-GGUF
Mistral-7B-OpenOrca-GGUF-32k-token-content (around 3.08 GB~7.7GB)=>https://huggingface.co/TheBloke/Mistral-7B-OpenOrca-GGUF


stable code =>https://ollama.ai/library/stable-code


Ming's Postman to test the general openAI API with local LLM => https://documenter.getpostman.com/view/3199697/2s9YsNdAEC
LiteLLM-huggingface use default=huggingface/bigcode/starcoder    (PS:Required HF_TOKEN,otherwise will has limitation   model=>huggingface/bigcode/starcoder   max_tokens=192  top_p=[0.0~0.9]  )

```







### Testing bash shell
```
curl http://192.168.0.232:3000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
     "model": "facebook--opt-1.3b",
     "messages": [{"role": "user", "content": "Say this is a test!"}],
     "temperature": 0.7
   }'
```




### Testing the OpenLLM
```
export OPENLLM_ENDPOINT=http://192.168.0.232:3000
openllm query 'What are large language models?'
```








### OpenAI and Local access URL
```
http://192.168.0.232:1234/v1/models
http://192.168.0.232:1234/metrics

http://192.168.0.232:3000/metrics
http://192.168.0.232:3000/v1/models

http://localhost:3000/metrics
http://localhost:3000/v1/models
https://api.openai.com/v1/models

```





### common docker command line
```
docker pull python
docker image ls
sudo docker container prune && docker image prune 
#for ubuntu
docker exec -it 1cfeec487615 /bin/bash
#for debian
docker exec -it 1cfeec487615 /usr/bin/bash

#Mapping window path refer:https://blog.51cto.com/u_16175478/8023989
docker run -itd --name ming_llm3 -v D:\work\repo:/home python:latest


docker run -d -it -p 22:22 --name ming_llm python:latest   
#docker run -v ./host/relative/path:/container/path
docker run --name ming_llm3 python:latest -v D:\work\repo:/home -itd  
docker run python:latest -v D:\work\repo:/home -itd

docker exec -itd  0c50843e44b4 /usr/bin/bash -p 22:22 python:latest -v D:\work\repo:/home/ming/



#How to Create a Docker Image From a Container refer:https://www.dataset.com/blog/create-docker-image/
#First convert your container to the docker images use => docker commit $YOUR_container_name
docker commit ming_llm3

#Retag you just commited the images_id to a real name(Optional)
docker tag $YOUR_container_name mingli512/ming_llm:latest

#Push your docker image to docker hub ($docker_hub_account_name/$project_name:$tagname)=> docker push [OPTIONS] NAME[:TAG]  please refer:https://docs.docker.com/engine/reference/commandline/push/
docker push mingli512/ming_llm:latest

```


### My local path
```
cd D:\work\repo\tmp\mingwork

```



### Sidan's server CLI
```
ssh sl6723@192.168.0.232
echo $OSTYPE - $(uname -srm)
cd /Users/sl6723/Documents/Ming/
tail -f /private/tmp/lmstudio-server-log.txt

docker pull python
docker pull ubuntu

sudo apt update && apt install net-tools curl telnet vim python3
apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list && apt update && apt install ngrok

ngrok config add-authtoken $Your_token
ngrok http --domain=airedale-native-chicken.ngrok-free.app 9000
ngrok http --domain=dashing-slowly-kiwi.ngrok-free.app 1234

ngrok tcp 9000
cloudflared tunnel --url localhost:11434/



===
docker pull litellm/ollama
docker run -d -p 8000:8000 --name litellm_ollama litellm/ollama
docker exec -it litellm_ollama /bin/bash
litellm --model ollama/llama2
http://192.168.0.232:8000


curl http://192.168.0.232:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
     "model": "ollama/llama2",
     "messages": [{"role": "user", "content": "Say this is a test!"}],
     "temperature": 0.7
   }'


====
docker pull ollama
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
docker exec -it ollama /bin/bash
http://192.168.0.232:11434

curl http://192.168.0.232:11434/api/generate -d '{
  "model": "llama2",
  "prompt":"Why is the sky blue?"
}'


docker commit ollama
docker tag 6c83a47c5972 mingli512/ming_ollama:latest


docker run -d -v /Users/sl6723/Documents/Ming:/home -p 80:80 --name ming_ollama python:latest
docker exec -it 3a5c5467c335 /bin/bash


======deprecated=====
sudo docker run  --name ming_ollama2 -v /Users/sl6723/Documents/Ming/:/home python:latest -itd
docker run --name ming_ollama5 python:latest -v /Users/sl6723/Documents/Ming/:/home -itd 
docker run   --name ming_ollama4 -v /Users/sl6723/Documents/Ming/:/home python:latest

```



### Princeton University Adroit temporary environment => https://myadroit.princeton.edu/pun/sys/dashboard
* Princeton University Adroit  VS IDE => https://myadroit.princeton.edu/pun/sys/dashboard/batch_connect/sessions
* Ollama pypi  =>https://pypi.org/project/ollama/
* Start the LLM Ollama service in PU's Adroit server. Please use instruction => https://github.com/aklakl/llm_sample/blob/master/ollamademo/README.md

```
#Princeton University Adroit Share folder /scratch/network
cd /scratch/network/sl6723/
cd /home/sl6723/repo/llm_sample   
cd /home/sl6723/.ollama/models
cd /home/sl6723/repo/llm_sample/ollamademo && bash run_ollama.sh

ps -ef | grep 'cloudflared\|ollama\|ngrok\|litellm'
netstat -aptn | grep '8000\|11434'

#Start the LiteLLM with Ollama
cd /scratch/network/sl6723/tmp/proc
ollama serve >>ollama.log &
ollama pull dolphin-phi
ollama run dolphin-phi >>dolphin-phi.log &
litellm --model ollama/dolphin-phi >>litellm.log &
cloudflared tunnel --url localhost:8000/ >>cloudflared.log &



#Quota limit warning for /home/sl6723    Using 10 GB of quota 10 GB. Consider deleting or archiving files to free up disk space. If you cannot free up enough space you can request more on this website: https://forms.rc.princeton.edu/quota
#Check your Storage Quota   refer:https://myadroit.princeton.edu/pun/sys/quota
du -sh  /home/sl6723  && du -h --max-depth=1 /home/sl6723 | sort -n -r | head -n 10  

#Check the special temporary space
ls -lah  /scratch/network | grep drwxrwxrwx

#Download 45.6GB file testing your local space 
wget https://huggingface.co/TheBloke/SG-Raccoon-Yi-200k-2.0-GGUF/resolve/main/sg-raccoon-yi-200k-2.0.Q6_K.gguf?download=true


```

### conda cli

```
#refer:https://docs.conda.io/projects/conda/en/latest/commands/clean.html
conda clean --all 

```