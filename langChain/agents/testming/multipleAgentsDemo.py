# refer:https://python.langchain.com/docs/modules/agents/agent_types/openai_multi_functions_agent

#original google AI: https://ai.google.dev/tutorials/python_quickstart?hl=en

import os
from langchain_google_genai import GoogleGenerativeAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper
from getpass import getpass

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API Key")
else:
    api_key = os.environ["GOOGLE_API_KEY"]
    print("GOOGLE_API_KEY already set to:", api_key) 


    
if "SERPAPI_API_KEY" not in os.environ:
    os.environ["SERPAPI_API_KEY"] = getpass.getpass("Provide your SERPAPI_API_KEY")
else:
    api_key = os.environ["SERPAPI_API_KEY"]
    print("SERPAPI_API_KEY already set to:", api_key)    
    
api_key = os.environ["GOOGLE_API_KEY"] #"AIzaSyAG9M9CFujKMKgUD1z_n-hLGozCs90ZTJ8"
print("GOOGLE_API_KEY=>", api_key)

os.environ["SERPAPI_API_KEY"] = getpass.getpass()



#==============================================
    
# llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=api_key)
# res = llm.invoke( "What are some of the pros and cons of Python as a programming language?")
# print("GoogleGenerativeAI.result=>",res)

llm = ChatGoogleGenerativeAI(model="gemini-pro")
result = llm.invoke("Write a ballad about LangChain")
print("ChatGoogleGenerativeAI.result=>", result)

#==============================================

#==============================================testingcode=========================

