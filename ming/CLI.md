* Ming's CLI


* Common customized base_url
```
base_url = "http://192.168.40.229:1234/v1"      #Sidan's local Server Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q8_0.gguf
base_url = "http://dashing-slowly-kiwi.ngrok-free.app/v1"      #Sidan's ngrok url 
base_url = "http://airedale-native-chicken.ngrok-free.app/v1"  # Seems like OpenLLM server only support SKD is openai==0.28  


```



* Common customized model
```
Ollama run saikatkumardey/tinyllama   (Ollama model around 903MB) => refer：https://ollama.ai/saikatkumardey/tinyllama 



ALL the Tiny models(Most model come from Huggingface)[PS: Tiny-Vicuna-1B-GGUF is working as well in colab]
Huggingface Tiny tinyllamas model gguf formating(around 1M refer:https://github.com/ggerganov/llama.cpp/issues/2708) => https://huggingface.co/klosax/tinyllamas-stories-gguf/blob/main/tinyllamas-stories-260k-f32.gguf
LocalDocs text embeddings model Necessary for LocalDocs feature Used for retrieval augmented generation (RAG)[around 40MB] =>https://gpt4all.io/models/gguf/all-MiniLM-L6-v2-f16.gguf
Huggingface =>https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
llama-tiny-Synthetic-therapist-GGUF (adapter_model.safetensors file around 49MB) => https://huggingface.co/wesley7137/llama-tiny-Synthetic-therapist-GGUF
LinguaMatic-Tiny-GGUF (Around 483MB~904MB) => https://huggingface.co/erfanzar/LinguaMatic-Tiny-GGUF
Tiny-Vicuna-1B-GGUF (around 482MB~1.17G) => https://huggingface.co/afrideva/Tiny-Vicuna-1B-GGUF
TinyLlama-1.1B-Chat-v0.3-GGUF(around 482MB~1.17G)  => https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v0.3-GGUF   (Huggingface-API https://huggingface.co/api/models/TheBloke/TinyLlama-1.1B-Chat-v0.3-GGUF/   TinyLlama introduction=>https://youtu.be/T5l228844NI)
TinyLlama-1.1B-1T-OpenOrca-GGUF(around 482MB~1.17G) => https://huggingface.co/TheBloke/TinyLlama-1.1B-1T-OpenOrca-GGUF
Huggingface tinyllamas  （bin file style around 438 MB） => https://huggingface.co/karpathy/tinyllamas



Ming's Postman to test the general openAI API with local LLM => https://documenter.getpostman.com/view/3199697/2s9YsNdAEC
LiteLLM-huggingface use default=huggingface/bigcode/starcoder    (PS:Required HF_TOKEN,otherwise will has limitation   model=>huggingface/bigcode/starcoder   max_tokens=192  top_p=[0.0~0.9]  )

```







* Testing bash shell
```
curl http://192.168.0.232:3000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
     "model": "facebook--opt-1.3b",
     "messages": [{"role": "user", "content": "Say this is a test!"}],
     "temperature": 0.7
   }'
```




* Testing the OpenLLM
```
export OPENLLM_ENDPOINT=http://192.168.0.232:3000
openllm query 'What are large language models?'
```





* OpenAI and Local access URL
```
http://192.168.0.232:1234/v1/models
http://192.168.0.232:1234/metrics

http://192.168.0.232:3000/metrics
http://192.168.0.232:3000/v1/models

http://localhost:3000/metrics
http://localhost:3000/v1/models
https://api.openai.com/v1/models

```





* common docker command line
```
docker pull python
docker image ls
sudo docker container prune
sudo docker image prune 
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


* My local path
```
cd D:\work\repo\tmp\mingwork

```



* Sidan's server CLI
```
ssh sl6723@192.168.0.232
echo $OSTYPE - $(uname -srm)
cd /Users/sl6723/Documents/Ming/
tail -f /private/tmp/lmstudio-server-log.txt

docker pull python
docker pull ubuntu

sudo apt update
sudo apt install net-tools curl telnet vim python3
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list && apt update && apt install ngrok

ngrok config add-authtoken $Your_token
ngrok http --domain=airedale-native-chicken.ngrok-free.app 9000
ngrok http --domain=dashing-slowly-kiwi.ngrok-free.app 1234

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


======deprescate=====
sudo docker run  --name ming_ollama2 -v /Users/sl6723/Documents/Ming/:/home python:latest -itd
docker run --name ming_ollama5 python:latest -v /Users/sl6723/Documents/Ming/:/home -itd 
docker run   --name ming_ollama4 -v /Users/sl6723/Documents/Ming/:/home python:latest

```
