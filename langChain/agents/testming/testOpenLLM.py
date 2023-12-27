#refer：https://python.langchain.com/docs/integrations/llms/openllm
#https://python.langchain.com/docs/integrations/providers/openllm
#OpenLLM => https://zhuanlan.zhihu.com/p/651130017

import os
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.llms import OpenLLM
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.tools import DuckDuckGoSearchRun
from langchain.tools import DuckDuckGoSearchResults
# Do this so we can see exactly what's going on under the hood
from langchain.globals import set_debug
from getpass import getpass

set_debug(True)


#==============================================Completed the setup env=========================


#==============================================exact logic code=========================
#Initialize LLM language model
## my own LLM API refer:https://python.langchain.com/docs/integrations/llms/openllm
server_url = "http://localhost:3000"  # Replace with remote host if you are running on a remote server
#server_url = "http://192.168.0.232:1234"  # Replace with remote host if you are running on a remote server
llm = OpenLLM(server_url=server_url)
#llm = OpenLLM(server_url='http://192.168.0.232:1234')

# llm = OpenLLM(
#     model_name="dolly-v2",
#     model_id="databricks/dolly-v2-3b",
#     temperature=0.94,
#     repetition_penalty=1.2,
# )

#=============testing OpenLLM==============
template = "What is a good name for a company that makes {product}?"
prompt = PromptTemplate(template=template, input_variables=["product"])
llm_chain = LLMChain(prompt=prompt, llm=llm)
generated = llm_chain.run(product="mechanical keyboard")
print("generated result=>",generated)
#=============testing OpenLLM==============
'''
# Initialize the general search API for search functionality
# Replace <your_api_key> in serpapi_api_key="<your_api_key>" with your actual SerpAPI key.
# search = SerpAPIWrapper()  #SerpAPI need license and charge the fee.
# search = DuckDuckGoSearchResults()  #SerpAPI need license and charge the fee.
search = DuckDuckGoSearchRun()  #SerpAPI need license and charge the fee.       

# Define a list of tools offered by the agent
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Useful when you need to answer questions about current events. You should ask targeted questions.",
    ),
]
#To make sure that our agent doesn’t get stuck in excessively long loops, we can set max_iterations. We can also set an early stopping method, which will determine our agent’s behavior once the number of max iterations is hit. By default, the early stopping uses method force which just returns that constant string. Alternatively, you could specify method generate which then does one FINAL pass through the LLM to generate an output.
agent_executor = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    max_iterations=20,
    early_stopping_method="generate",
)

agent_executor.run("what is the lastest progress in membrane distillation technology in 2023?")

#agent_executor.run("What date time is right now with full timezone and area ?")
'''
#==============================================exact logic code=========================