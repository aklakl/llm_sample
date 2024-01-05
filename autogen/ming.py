import autogen
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json


#autogen 
#==========================
# Load LLM inference endpoints from an env variable or a file
# See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
# and OAI_CONFIG_LIST_sample
# config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
# refer:https://github.com/microsoft/autogen

#Custom configurations
#base_url = "http://localhost:1234/v1"  # You can specify API base URLs if needed. eg: localhost:8000
#http://10.9.150.174:1234/v1/models
base_url = "http:// 10.16.97.15:1234/v1"  #Sidan's Server Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q8_0.gguf
#base_url = "http://airedale-native-chicken.ngrok-free.app/v1"  # OpenLLM server refer: https://colab.research.google.com/drive/1GKlfU7Fjq30oQPirHvCcQy_e_B8vNEDs?usp=sharing
api_type = "openai"  # Type of API, e.g., "openai" or "aoai".
api_version = None  # Specify API version if needed.
#api_model= "palm/chat-biso"
api_model="NousResearch--Nous-Hermes-llama-2-7b"
api_key = "None"

config_list_structure = [
    {
        "model": "gpt-4",
        "api_key": "<your OpenAI API key here>"
    },
    {
        "model": "gpt-4",
        "api_key": "<your OpenAI API key here>"
    },
    {
        "model": "Llama-2-7B-Chat-GGML",
        "api_key": "<your Azure OpenAI API key here>",
        "base_url": "http://localhost:1234/v1",
        "api_type": "azure",
        "api_version": "2023-07-01-preview"
    },
    {
        "model": "<your Azure OpenAI deployment name>",
        "api_key": "<your Azure OpenAI API key here>",
        "base_url": "<your Azure OpenAI API base here>",
        "api_type": "azure",
        "api_version": "2023-07-01-preview"
    },
    {
        "model": "<your Azure OpenAI deployment name>",
        "api_key": "<your Azure OpenAI API key here>",
        "base_url": "<your Azure OpenAI API base here>",
        "api_type": "azure",
        "api_version": "2023-07-01-preview"
    }
]
log_msg = "Configuration List config_list_structure=>"
#print(f"{log_msg} {config_list_structure}")




# # refer: https://microsoft.github.io/autogen/docs/reference/oai/openai_utils/
# api_keys = []
# base_urls = []
# api_types = []
# api_versions =[]
# config_list2 = autogen.get_config_list(
#     api_keys=api_keys,
#     base_urls=base_urls,
#     api_type=api_types,
#     api_version=api_versions
# )


#Static config_list2 
config_list2 = [
    {
    "model":api_model,
    "base_url":base_url,
    "api_version":api_version,
    "api_key":api_key
    }
]
log_msg = "Configuration List2:"
print(f"{log_msg} {config_list2}")


# assistant = AssistantAgent("assistant", llm_config={"config_list": config_list2})
# user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding"})
# user_proxy.initiate_chat(assistant, message="Plot a chart of NVDA and TESLA stock price change YTD.")
# ##==========================

# assistant = AssistantAgent("assistant", llm_config={"api_key": "ming's key","base_url": base_url,"api_model":api_model})
# user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding"})
# #user_proxy.initiate_chat(assistant, message="Show me the YTD gain of 10 largest technology companies as of today.")
# user_proxy.initiate_chat(assistant, message="Plot a chart of NVDA and TESLA stock price change YTD.")
# # This triggers automated chat to solve the task



#==========================
# create an AssistantAgent named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "cache_seed": 42,  # seed for caching and reproducibility
        "config_list": config_list2,  # a list of OpenAI API configurations
        "temperature": 0,  # temperature for sampling
    },  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
)
# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,  # set to True or image name like "python:3" to use docker
    },
)
# the assistant receives a message from the user_proxy, which contains the task description
user_proxy.initiate_chat(
    assistant,
    message="""What date is today? Compare the year-to-date gain for META and TESLA.""",
)


