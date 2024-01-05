#import autogen
from autogen import AssistantAgent, UserProxyAgent, oai

config_list = [
    {"model":"palm/chat-bison",
    "api_base":"https://airedale-native-chicken.ngrok-free.app",
    "api_type":"open_ai",
    "api_version":""
    }
]

log_msg = "Configuration List:"
print(f"{log_msg} {config_list}")

# # WARNING - Completion.create is deprecated in pyautogen v0.2 and openai>=1. The new openai requires initiating a client for inference. Please refer to https://microsoft.github.io/autogen/docs/Use-Cases/enhanced_inference#api-unification
# response = oai.Completion.create(config_list=config_list , prompt="Hi")
# print(response)


llm_config={
    "config_list":config_list
}

assistant = AssistantAgent("assistant",llm_config=llm_config)
user_proxy = UserProxyAgent("user_proxy")
user_proxy.initiate_chat(assistant, message="Plot a chart of NVDA and TESLA stock price change YTD.")



#==========================
'''

assistant = AssistantAgent("assistant", llm_config={"api_key": "ming's key","base_url": "http://localhost:1234/v1"})
user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding"})
#user_proxy.initiate_chat(assistant, message="Show me the YTD gain of 10 largest technology companies as of today.")
user_proxy.initiate_chat(assistant, message="Plot a chart of NVDA and TESLA stock price change YTD.")
# This triggers automated chat to solve the task

'''
#==========================