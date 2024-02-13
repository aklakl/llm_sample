#@title Python code(Need to conside about the openai timeout situation)
#code refer:https://colab.research.google.com/drive/11ju2Hg0GmjVyxEBsQ30FiwdZyugANHP1?usp=sharing


import os
import time
from openai import OpenAI
import autogen
from autogen import AssistantAgent, UserProxyAgent, oai
# using datetime module
import datetime;


#===========================================================
#This code required openai>1.0.0 (base_url)
#os.environ["OPENAI_API_KEY"] = "YOUR KEY"
#g_base_url = "http://2.tcp.ngrok.io:10864/v1"  #LM Studio server in PU's IAC lab local IP address is => http://128.112.73.83:1234/v1/models
g_base_url = "https://dna-brook-significantly-industry.trycloudflare.com/v1"  #LLM services build by Ming-TextGen-GPU=> https://colab.research.google.com/drive/1-pUeLBWvsh0M82OhaXivZigVhtJKhPm_?usp=sharing
g_api_key = "sk-llllllllllllllllllllll"  # even your local don't use the authorization, but you need to fill something, otherwise will be get exception.
g_api_model="stablelm-zephyr-3b.Q6_K" #stablelm-zephyr-3b.Q6_K.gguf  TheBloke/stablelm-zephyr-3b-GGUF/stablelm-zephyr-3b.Q6_K.gguf
g_api_model="gpt-3.5-turbo"
os.environ["OPENAI_API_KEY"] = g_api_key
os.environ["OPENAI_API_BASE"] = g_base_url

g_config_list = [
    {
        "model":g_api_model,
        "base_url":g_base_url,
        "api_type":"open_ai"
    }
]


g_task_message="Build the requirement of a Web shopping system(It include User Authentication and Authorization/User registration and login functionality/Product Management/Shopping Cart/Order Processing/Search and Navigation/ include the Design document)"


#=========


# config_list_gpt4 = autogen.config_list_from_json(
#     "OAI_CONFIG_LIST",
#     filter_dict={
#         "model": ["gpt-4", "gpt-4-0314", "gpt4", "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"],
#     },
# )


#===========================================================


# timestamp = time.time()
# print("Timestamp:", timestamp)
#print("config_list_gpt4 =>",config_list_gpt4)



def run_autogen_main():
    print("=====================starting run_autogen_main============================ use g_base_url=>",g_base_url)
    #print("g_config_list=>",g_config_list)
    #llm_config = {"config_list": config_list_gpt4, "cache_seed": 42}
    llm_config = {"config_list": g_config_list, "cache_seed": 42}

    #autogen.ChatCompletion.start_logging()   #refer:https://medium.com/@krtarunsingh/mastering-autogen-a-comprehensive-guide-to-next-generation-language-model-applications-b375d9b4dc6d
    user_proxy = autogen.UserProxyAgent(
        name="User_proxy",
        system_message="A human admin.",
        #description="A human admin.",
        code_execution_config={
            "last_n_messages": 2,
            "work_dir": "groupchat",
            "use_docker": False,
        },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
        #max_consecutive_auto_reply=0,  # terminate without auto-reply
        #human_input_mode="TERMINATE",
        human_input_mode="NEVER",
    )

    ba = autogen.AssistantAgent(
        name="Business analyst",
        system_message="Creative in software product ideas. Provide the proposals with more detail and requirement",
        #description="Creative in software product ideas. Provide the proposals with more detail and requirement",
        llm_config=llm_config,
    )

    pm = autogen.AssistantAgent(
        name="Product_manager",
        system_message="Oversee and rectify proposals provided by the business analyst.",
        #description="Oversee and rectify proposals provided by the business analyst.",
        llm_config=llm_config,
    )
    #speaker_selection_method="manual"  refer:https://github.com/microsoft/autogen/issues/842#issuecomment-1873480277
    groupchat = autogen.GroupChat(agents=[user_proxy, ba, pm], messages=[], max_round=20)
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    user_proxy.initiate_chat(
        manager, message=g_task_message
    )
    # type exit to terminate the chat
    #autogen.ChatCompletion.stop_logging()


    print("=====================completed run_autogen_main============================")




def run_autogen_coder():
    print("=====================starting run_autogen_main============================")
    #print("g_config_list=>",g_config_list)
    #llm_config = {"config_list": config_list_gpt4, "cache_seed": 42}
    llm_config = {"config_list": g_config_list, "cache_seed": 42}

    user_proxy = autogen.UserProxyAgent(
        name="User_proxy",
        system_message="A human admin.",
        code_execution_config={
            "last_n_messages": 2,
            "work_dir": "groupchat",
            "use_docker": False,
        },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
        human_input_mode="TERMINATE",

    )

    coder = autogen.AssistantAgent(
        name="Coder",
        llm_config=llm_config,
    )

    pm = autogen.AssistantAgent(
        name="Product_manager",
        system_message="Creative in software product ideas.",
        llm_config=llm_config,
    )

    groupchat = autogen.GroupChat(agents=[user_proxy, coder, pm], messages=[], max_round=12)
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    user_proxy.initiate_chat(
        manager, message="Find a latest paper about gpt-4 on arxiv and find its potential applications in software."
    )
    # type exit to terminate the chat


    print("=====================completed run_autogen_main============================")




'''
This code required openai>1.0.0 :
'''
def run_simple_test_autogen():
    print("=====================starting run_simple_test_autogen============================")
    config_list = [
        {
            "model":"palm/chat-bison",
            "base_url":g_base_url,
            "api_type":"open_ai"
        }
    ]

    log_msg = "Configuration List:"
    print(f"{log_msg} {config_list}")

    llm_config={
        "config_list":config_list
    }
    assistant = AssistantAgent("assistant",llm_config=llm_config)
    user_proxy = UserProxyAgent("user_proxy")
    user_proxy.initiate_chat(assistant, message="Plot a chart of NVDA and TESLA stock price change YTD.")
    print("=====================completed run_simple_test_autogen============================")





'''
This code required openai>1.0.0 :
'''
def run_test_openai_completion():
    print("=====================starting run_test_openai_completion============================")
    try:
        # Point to the local server
        client = OpenAI(base_url=g_base_url, api_key=g_api_key)
        #client = OpenAI()
        #openai.Completion.acreate() #This is openai 0.x.x version style. and openai version 1.X.X refer:https://pypi.org/project/openai/
        completion = client.chat.completions.create(model=g_api_model, messages=[{"role": "user", "content": "Who are you?"}])
        print(completion.choices[0].message.content)
    except Exception as e:
        print(f"""run_test_openai_completion failed with Exception{e}. \n""")
    print("=====================completed run_test_openai_completion============================")


def run_test_print_during():
    print("=====================starting run_test_print_during============================")
    from datetime import datetime

    # Define two date times
    start_time = datetime(2023, 1, 1, 12, 0, 0)
    end_time = datetime.now()  # 当前时间

    # Calculate time difference
    time_difference = end_time - start_time

    # Printing time difference
    print("Time Difference:", time_difference)
    print("Days:", time_difference.days)
    print("Seconds:", time_difference.seconds)
    print("=====================completed run_test_print_during============================")




def run_openai_vision_example():
    print("=====================Starting run_openai_vision_example============================")
    #=======
    # Adapted from OpenAI's Vision example
    from openai import OpenAI
    import base64
    import requests

    # Point to the local server
    client = OpenAI(base_url=g_base_url, api_key="not-needed")

    # Ask the user for a path on the filesystem:
    path = input("Enter a local filepath to an image: ")

    # Read the image and encode it to base64:
    base64_image = ""
    try:
      image = open(path.replace("'", ""), "rb").read()
      print("image=>",image)
      base64_image = base64.b64encode(image).decode("utf-8")
      print("base64_image=>",base64_image)
    except:
      print("Couldn't read the image. Make sure the path is correct and the file exists.")
      exit()

    completion = client.chat.completions.create(
      model="local-model", # not used
      messages=[
        {
          "role": "system",
          "content": "This is a chat between a user and an assistant. The assistant is helping the user to describe an image.",
        },
        {
          "role": "user",
          "content": [
            {"type": "text", "text": "What’s in this image?"},
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              },
            },
          ],
        }
      ],
      max_tokens=1000,
      stream=True
    )

    for chunk in completion:
      if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
    #=======
    print("=====================completed run_openai_vision_example============================")


def start_logging():
    # ct stores current time
    ct = datetime.datetime.now()
    #print("current time:-", ct)
    
    # ts store timestamp of current time
    ts = ct.timestamp()
    #print("timestamp:-", ts)
    print("=====current time:-",ct,"|timestamp:-",ts)
    return ts

#Running
if __name__ == "__main__":
    start_logging()
    #run_test_print_during()
    #run_test_openai_completion()
    #run_simple_test_autogen();
    #run_openai_vision_example()
    #run_autogen_coder()
    run_autogen_main()

    start_logging()
    print("===========completed=============",__name__)


