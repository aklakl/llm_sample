import autogen
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json


#autogen 
#==========================
# Load LLM inference endpoints from an env variable or a file
# See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
# and OAI_CONFIG_LIST_sample
# config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
# refer:https://github.com/microsoft/autogen
config_list = [
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
log_msg = "Configuration List:"
print(f"{log_msg} {config_list}")

api_keys = ["YOUR_OPENAI_API_KEY"]
#base_urls = "http://localhost:1234/v1"  # You can specify API base URLs if needed. eg: localhost:8000
#http://10.9.150.174:1234/v1/models
base_urls = "http://10.9.150.174:1234/v1/"  #Sidan's Server Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q8_0.gguf
api_type = "openai"  # Type of API, e.g., "openai" or "aoai".
api_version = None  # Specify API version if needed.

config_list2 = autogen.get_config_list(
    api_keys=api_keys,
    base_urls=base_urls,
    api_type=api_type,
    api_version=api_version
)

log_msg = "Configuration List2:"
print(f"{log_msg} {config_list2}")
# assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})
# user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding"})
# user_proxy.initiate_chat(assistant, message="Plot a chart of NVDA and TESLA stock price change YTD.")
#==========================

assistant = AssistantAgent("assistant", llm_config={"api_key": "ming's key","base_url": "http://localhost:1234/v1"})
user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding"})
#user_proxy.initiate_chat(assistant, message="Show me the YTD gain of 10 largest technology companies as of today.")
user_proxy.initiate_chat(assistant, message="Plot a chart of NVDA and TESLA stock price change YTD.")
# This triggers automated chat to solve the task

