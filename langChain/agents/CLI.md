* multipleAgentsDemo Command
conda create --name minglocalenv3.9 python=3.9
conda activate minglocalenv3.9
conda deactivate
conda info --env
pip install langchain==0.0.352
pip show langchain
!pip install openai openllm google-search-results langchain langchain-google-genai beautifulsoup4


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

