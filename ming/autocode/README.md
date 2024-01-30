# The code with autocode with dev
```

```

### Running Locally

1. Go to Google colab Start the ngrok mapping litellm server first refer => https://colab.research.google.com/drive/1GKlfU7Fjq30oQPirHvCcQy_e_B8vNEDs?usp=sharing    
Or use LM Studio build your local LLM => https://lmstudio.ai/


2. Run your code local machine:
```
export OPENAI_API_KEY=sk-1111111111111111111
export OPENAI_API_BASE=http://airedale-native-chicken.ngrok-free.app/v1

pip install -r requirements.txt --use-deprecated=legacy-resolver

python3.12 -m venv autocode
source autocode/bin/activate
# deactivate

python llm_sample/ming/autocode/autocode.py



```
### Running AutoGen version

```
https://colab.research.google.com/drive/11ju2Hg0GmjVyxEBsQ30FiwdZyugANHP1?usp=sharing

```


=====
AgentDev project Solution:

Agent:
We want to build project with Websites 
The requirement follow this:
#.Web shopping system(It include User Authentication and Authorization/User registration and login functionality/Product Management/Shopping Cart/Order Processing/Search and Navigation/ include the Design document)
#.Using python language

Resources:
Code Llama is a code-specialized version of Llama 2 refer:https://about.fb.com/news/2023/08/code-llama-ai-for-coding/
Code Llama – Python is a language specialized variation of Code Llama,


ChatDev 
1.Always got exception,May be 4k+ context token issue?(PS:My openai services based on TextGen currently only 2k context token , refer:https://colab.research.google.com/drive/1-pUeLBWvsh0M82OhaXivZigVhtJKhPm_?usp=sharing)
2.Have not see any place can define the agent through the LLM service.
3.


MetaGPT?
1.
2.
3.






Undo task:
1.Find any agent framework can be more flexable
ANSWER:So far seems like langchain is more flexable compare to AutoGen、CrewAI、MetaGPT
https://github.com/microsoft/autogen/blob/7265ef1a3fb194e1d3d7345e47e4dc9a30ecd6fd/notebook/agentchat_gemini.ipynb
https://github.com/PradipNichite/Youtube-Tutorials/blob/main/Langchain_Agents_SQL_Database_Agent.ipynb


Done--2.Provide 4k token content model.
ANSWER:Yi models support up to 200k context (you have to download the 200k models specifically). Mistral/Mixtral supports up to 32k.Llama 2-7B also support 4k  context
refer:https://www.reddit.com/r/LocalLLaMA/comments/18moo27/recommendations_on_locally_runnable_llms_with/
3.




