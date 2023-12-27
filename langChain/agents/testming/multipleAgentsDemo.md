* multipleAgentsDemo Command
conda create --name minglocalenv python=3.11
conda activate minglocalenv
pip install langchain==0.0.352
pip show langchain
pip install openai google-search-results langchain-google-genai
!pip install langchain-google-genai

python3 multipleAgentsDemo.py