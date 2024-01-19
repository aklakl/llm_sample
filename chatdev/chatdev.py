import os
from openai import OpenAI





# from langchain.tools import DuckDuckGoSearchRun
# search_tool = DuckDuckGoSearchRun()


#os.environ["OPENAI_API_KEY"] = "YOUR KEY"
g_base_url = "http://192.168.137.176:1234/v1"  #Sidan's Server Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q8_0.gguf
g_api_key = "sk-llllllllllllllllllllll"  # even your local don't use the authorization, but you need to fill something, otherwise will be get exception.
#g_base_url = "http://airedale-native-chicken.ngrok-free.app/v1"  # Seems like OpenLLM server only support SKD is openai==0.28  pyautogen==0.1.14 . refer: https://colab.research.google.com/drive/1GKlfU7Fjq30oQPirHvCcQy_e_B8vNEDs?usp=sharing
#g_api_model="NousResearch--Nous-Hermes-llama-2-7b"
g_api_model="TinyLlama--TinyLlama-1.1B-Chat-v1.0"
os.environ["OPENAI_API_KEY"] = g_api_key
os.environ["OPENAI_API_BASE"] = g_base_url


'''
This code required openai>1.0.0 :
'''
def run_test_openai_completion():
    print("=====================starting run_test_openai_completion============================")
    try:
        # Point to the local server
        #client = OpenAI(base_url=g_base_url, api_key=g_api_key)
        client = OpenAI()
        #openai.Completion.acreate() #This is openai 0.x.x version style. and openai version 1.X.X refer:https://pypi.org/project/openai/
        completion = client.chat.completions.create(model=g_api_model, messages=[{"role": "user", "content": "Who are you?"}])
        print(completion.choices[0].message.content)
    except Exception as e:
        print(
            f"""
            run_test_openai_completion failed with Exception{e}. \n"""
        )  
    print("=====================completed run_test_openai_completion============================")    


#running main method
if __name__ == "__main__":
    run_test_openai_completion()
    print("===========completed=============",__name__)