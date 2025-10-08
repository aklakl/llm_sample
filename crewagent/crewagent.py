import os
from crewai import Agent, Task, Crew, Process
from openai import OpenAI




# You can choose to use a local model through Ollama for example.
#
# from langchain.llms import Ollama
# ollama_llm = Ollama(model="openhermes")

# Install duckduckgo-search for this example:
# !pip install -U duckduckgo-search

from langchain.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()


#os.environ["OPENAI_API_KEY"] = "YOUR KEY"
g_base_url = "http://192.168.137.176:1234/v1"  #Sidan's Server Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q8_0.gguf
g_api_key = "sk-llllllllllllllllllllll"  # even your local don't use the authorization, but you need to fill something, otherwise will be get exception.
#g_base_url = "http://airedale-native-chicken.ngrok-free.app/v1"  # Seems like OpenLLM server only support SKD is openai==0.28  pyautogen==0.1.14 . refer: https://colab.research.google.com/drive/1GKlfU7Fjq30oQPirHvCcQy_e_B8vNEDs?usp=sharing
#g_api_model="NousResearch--Nous-Hermes-llama-2-7b"
g_api_model="TinyLlama--TinyLlama-1.1B-Chat-v1.0"
os.environ["OPENAI_API_KEY"] = g_api_key
os.environ["OPENAI_API_BASE"] = g_base_url


def run_crewai_agent():
    print("=====================starting run_crewai_agent============================")
    # Define your agents with roles and goals
    researcher = Agent(
      role='Senior Research Analyst',
      goal='Uncover cutting-edge developments in AI and data science',
      backstory="""You work at a leading tech think tank.
      Your expertise lies in identifying emerging trends.
      You have a knack for dissecting complex data and presenting
      actionable insights.""",
      verbose=True,
      allow_delegation=False,
      tools=[search_tool]
      # You can pass an optional llm attribute specifying what mode you wanna use.
      # It can be a local model through Ollama / LM Studio or a remote
      # model like OpenAI, Mistral, Antrophic of others (https://python.langchain.com/docs/integrations/llms/)
      #
      # Examples:
      # llm=ollama_llm # was defined above in the file
      # llm=ChatOpenAI(model_name="gpt-3.5", temperature=0.7)
    )
    writer = Agent(
      role='Tech Content Strategist',
      goal='Craft compelling content on tech advancements',
      backstory="""You are a renowned Content Strategist, known for
      your insightful and engaging articles.
      You transform complex concepts into compelling narratives.""",
      verbose=True,
      allow_delegation=True,
      # (optional) llm=ollama_llm
    )

    # Create tasks for your agents
    task1 = Task(
      description="""Conduct a comprehensive analysis of the latest advancements in AI in 2024.
      Identify key trends, breakthrough technologies, and potential industry impacts.
      Your final answer MUST be a full analysis report""",
      agent=researcher
    )

    task2 = Task(
      description="""Using the insights provided, develop an engaging blog
      post that highlights the most significant AI advancements.
      Your post should be informative yet accessible, catering to a tech-savvy audience.
      Make it sound cool, avoid complex words so it doesn't sound like AI.
      Your final answer MUST be the full blog post of at least 4 paragraphs.""",
      agent=writer
    )

    # Instantiate your crew with a sequential process
    crew = Crew(
      agents=[researcher, writer],
      tasks=[task1, task2],
      verbose=2, # You can set it to 1 or 2 to different logging levels
    )

    # Get your crew to work!
    result = crew.kickoff()

    print("######################")
    print(result)



'''
This code required openai>1.0.0 :
'''
def run_test_openai_completion():
    print("=====================starting run_test_openai_completion============================")
    try:
        # Point to the local server
        client = OpenAI(base_url=g_base_url, api_key=g_api_key)
        #openai.Completion.acreate() #This is openai 0.x.x version style. and openai version 1.X.X refer:https://pypi.org/project/openai/
        completion = client.chat.completions.create(model=g_api_model, messages=[{"role": "user", "content": "Who are you?"}])
        print(completion.choices[0].message.content)
    except Exception as e:
        print(
            f"""
            run_test_openai_completion failed with Exception{e}. \n"""
        )  
    print("=====================completed run_test_openai_completion============================")    


def run_test_openai():
    print("=====================starting run_test_openai============================")
    # Point to the local server
    client = OpenAI(base_url=g_base_url, api_key=g_api_key)

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
            {"type": "text", "text": "Say this is a test"}
          ],
        }
      ],
      max_tokens=2000,
      stream=True
    )

    for chunk in completion:
      if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
    print("=====================completed run_test_openai============================")

#running main method
if __name__ == "__main__":
    run_crewai_agent()
    #run_test_openai()
    #run_openai_completion()
    print("===========completed=============",__name__)