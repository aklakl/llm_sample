import ollama

print("ollama lib=>",ollama)
#refer:https://pypi.org/project/ollama/
def run_ollama():
    response = ollama.chat(model='phi', messages=[{'role': 'user', 'content': 'Why is the sky blue?'}])
    print("response=>",response)


#Running
if __name__ == "__main__":
    run_ollama()
    print("===========completed=============",__name__)
