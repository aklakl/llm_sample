* multipleAgentsDemo Command
conda create --name minglocalenv3.9 python=3.9
conda activate minglocalenv3.9
conda deactivate
conda info --env
pip install langchain==0.0.352
pip show langchain
!pip install openai openllm google-search-results langchain langchain-google-genai beautifulsoup4


* Other command
python3 testming/multipleAgentsDemo.py

* localLLM
python3.11 localLLM/testOpenLLM.py
python3 localLLM/openAI_example.py
python3 localLLM/testOldOpenAI.py
python3 localLLM/testOpenAI.py


python3 searchAPI.py
python3 searchBaidu.py
python3 searchGoogle.py

* selfAskWithSearch
python3 selfAskWithSearch/selfAskWithSearch.py

