* Ming's CLI
```
base_url = "http://192.168.40.229:1234/v1"  #Sidan's Server Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q8_0.gguf
base_url = "http://airedale-native-chicken.ngrok-free.app/v1"  # Seems like OpenLLM server only support SKD is openai==0.28  

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


* local path
```
cd D:\work\repo\tmp\mingwork

```
