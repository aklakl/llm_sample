* multipleAgentsDemo Command
conda create --name minglocalenv3.9 python=3.9
conda activate minglocalenv3.9
conda deactivate
conda info --env
pip install langchain==0.0.352
pip show langchain
!pip install openai openllm google-search-results langchain langchain-google-genai beautifulsoup4
pip install -r requirements.txt


* Other command
python3 agents/testming/multipleAgentsDemo.py

* localLLM
python3.11 localLLM/testOpenLLM.py
python3 localLLM/openAI_example.py
python3 localLLM/testOldOpenAI.py
python3 localLLM/testOpenAI.py
python3 localLLM/testOpenLLM.py

python3 searchAPI.py
python3 searchBaidu.py
python3 searchGoogle.py

* selfAskWithSearch
python3 selfAskWithSearch/selfAskWithSearch.py

* Testing bash shell
curl http://192.168.0.232:3000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
     "model": "facebook--opt-1.3b",
     "messages": [{"role": "user", "content": "Say this is a test!"}],
     "temperature": 0.7
   }'

* Testing the OpenLLM
export OPENLLM_ENDPOINT=http://192.168.0.232:3000
openllm query 'What are large language models?'

* OpenAI and Local access URL
http://192.168.0.232:1234/v1/models
http://192.168.0.232:1234/metrics

http://192.168.0.232:3000/metrics
http://192.168.0.232:3000/v1/models

http://localhost:3000/metrics
http://localhost:3000/v1/models
https://api.openai.com/v1/models



=============================
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
=============================