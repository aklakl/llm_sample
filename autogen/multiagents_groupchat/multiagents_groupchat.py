# AutoGen agentchat_multiagents_groupchat => https://youtu.be/u9RYO551G9Q?t=183
# https://microsoft.github.io/autogen/docs/Use-Cases/agent_chat
# https://microsoft.github.io/autogen/docs/FAQ/#code-execution

import autogen
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json, oai
import openai


#Initial your Custom llm_config configurations,LM Studio Server support SKD is openai==0.28  pyautogen==0.1.14 . refer: https://colab.research.google.com/drive/1GKlfU7Fjq30oQPirHvCcQy_e_B8vNEDs?usp=sharing
# base_url = "http://airedale-native-chicken.ngrok-free.app/v1"  # Seems like OpenLLM server only support SKD is openai==0.28  pyautogen==0.1.14 . refer: https://colab.research.google.com/drive/1GKlfU7Fjq30oQPirHvCcQy_e_B8vNEDs?usp=sharing
# api_model="TinyLlama--TinyLlama-1.1B-Chat-v1.0"
base_url = "http://192.168.0.232:1234/v1"  #Sidan's Server Mistral-7B-Instruct-v0.2-GGUF/mistral-7b-instruct-v0.2.Q6_K.gguf
api_model="Mistral-7B-Instruct-v0.2-GGUF/mistral-7b-instruct-v0.2.Q6_K.gguf"
api_key = "sk-llllllllllllllllllllll"   #openai==0.28 key style must be like this,Even your local LLM doesn't use it also follow the key style. refer:https://pypi.org/project/openai/0.28.0/
# default_global_llm_config_list with parameters
default_global_llm_config_list = [
    {
    "model":api_model,
    "api_base":base_url,
    "api_version":None,
    "api_key":api_key
    }
]


# hardcode default_global_llm_config_list
# default_global_llm_config_list = [
#     {
#     "model":"Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q8_0.gguf",
#     "api_base":"http://192.168.0.232:1234/v1",
#     "api_version":None,
#     "api_key":"sk-llllllllllllllllllllll"
#     }
# ]


def run_agentchat_multiagents_groupchat():
#    try:
        #Base on openai==0.28  pyautogen==0.1.14 ,If you want to use your own LLM,you must be override your openai.api_base and openai.api_key for autogen, otherwise won't be work.
        openai.api_key = api_key  # supply your API key however you choose
        openai.api_base= base_url # supply your api base URL If you have your own LLM
        openai.model = api_model  # supply your api base URL If you have your own model (PS:openLLM required change the model,LM Studio doesn't care about model)

        #print("autogen.oai.openai_utils.get_config_list=>",oai.openai_utils.get_config_list())

        #
        verify_autogen_and_openai_basic_info()
        autogen.ChatCompletion.start_logging()

        #code_execution_config= False,
        llm_config = default_global_llm_config_list
        user_proxy = autogen.UserProxyAgent(
            llm_config=llm_config,
            name="user_proxy",
            human_input_mode="NEVER",
            system_message="A human admin,",
            code_execution_config={
                "work_dir": "groupchat",
                "last_n_message": 2, 
            },
            default_auto_reply="Sorry, I couldn't process that request. Could you try another solution?",  # Set a default auto-reply message here, refer:https://github.com/microsoft/autogen/issues/279#issuecomment-1783656203
        )
        # user_proxy.reset()
        # user_proxy.clear_history()

        coder = autogen.AssistantAgent(
            name="Coder",
            code_execution_config={"work_dir": "coding","last_n_message": 2 },
            llm_config=llm_config,
        )

        pm = autogen.AssistantAgent(
            name="Product_manager",
            system_message="Creative in product ideas",
            llm_config=llm_config,
        )

        # refer:https://microsoft.github.io/autogen/docs/reference/agentchat/groupchat/
        groupchatins = autogen.GroupChat(agents=[user_proxy,coder,pm],messages=[],max_round=15)
        manager = autogen.GroupChatManager(groupchat=groupchatins,llm_config=llm_config)

        user_proxy.initiate_chat(
            manager,
            #message="Query the latest news on yahoo.com,randomly pick one about TESLA,scrape the article content,and form a post for writing a blog",
            message="Query today's weather in Princeton new jersey USA",
            llm_config=llm_config,
        )
        autogen.ChatCompletion.stop_logging()
        print(f"==========completed run_agentchat_multiagents_groupchat=============\n")   
#    except Exception as e:
#        print(f"""run_agentchat_multiagents_groupchat failed with Exception{e}. \n""")   



#Troubleshooting utils method
def verify_autogen_and_openai_basic_info():
    print("====================")
    #check openai basic_info
    print("openai.Model.list=>",openai.Model.list())

    #check autogen basic_info
    print("autogen.__version__=>",autogen.__version__)
    # print("autogen.oai.openai_utils.get_config_list=>",autogen.oai.openai_utils.get_config_list())
    print("====================")


#run_troubleshooting_openai is debuging for run_agentchat_multiagents_groupchat method
def run_troubleshooting_openai():
    openai.api_key = api_key  # supply your API key however you choose
    openai.api_base= base_url # supply your api base URL If you have your own LLM
    openai.model = api_model  # supply your api base URL If you have your own model (PS:openLLM required change the model,LM Studio doesn't care about model)
    request_timeout = 3000
    try:
        #
        verify_autogen_and_openai_basic_info()

        #response = openai.Completion.create(request_timeout=request_timeout, **config)


        # create a chat completion also work as well
        response = openai.ChatCompletion.create(model=api_model, messages=[{"role": "user", "content": "Hello world"}])

        #openai.Completion.create. This is working as well.
        #response = openai.Completion.create(model=api_model, prompt="Hello world")
        print("openai.Completion.response=>",response)
    except Exception as e:
        print(f"Error: {e}")
        print(f"Response: {e.response}")
        raise  # Re-raise the exception for further investigation





#Main entry
if __name__ == "__main__":
    run_agentchat_multiagents_groupchat()
    # run_troubleshooting_openai()

