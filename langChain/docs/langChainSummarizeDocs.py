# refer:https://github.com/sugarforever/LangChainSummarizeYoutubeTranscript/blob/main/Summarize_With_Loaders.ipynb
# pip install openai
# pip install openllm
# pip install langchain==0.0.139
# pip install unstructured
# pip install tiktoken
# pip install tiktoken, unstructured, openllm, openai,langchain
# pip install -r requirements.txt --use-deprecated=legacy-resolver
# conda install -c conda-forge langchain unstructured tiktoken openllm openai

# langchain==0.0.139  langchain versions=>https://pypi.org/project/langchain/#history

import os
from langchain.document_loaders import UnstructuredURLLoader, UnstructuredPowerPointLoader, ReadTheDocsLoader, PyPDFLoader
#from langchain.document_loaders import SeleniumURLLoader
#from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.callbacks import get_openai_callback
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenLLM

def summarize_docs(docs, doc_url):
    print (f'You have {len(docs)} document(s) in your {doc_url} data')
    print (f'There are {len(docs[0].page_content)} characters in your document')

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    split_docs = text_splitter.split_documents(docs)

    print (f'You have {len(split_docs)} split document(s)')

    ##OpenAI
    # OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
    # llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name="text-davinci-003")
    
    ## my own LLM API refer:https://python.langchain.com/docs/integrations/llms/openllm
    # server_url = "http://localhost:3000"  # Replace with remote host if you are running on a remote server
    server_url = "http://192.168.0.232:1234"  # Replace with remote host if you are running on a remote server
    llm = OpenLLM(server_url=server_url)
    # llm = OpenLLM(
    #     model_name="dolly-v2",
    #     model_id="databricks/dolly-v2-3b",
    #     temperature=0.94,
    #     repetition_penalty=1.2,
    # )
    

    chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=False)

    response = ""
    with get_openai_callback() as cb:
        response = chain.run(input_documents=split_docs)
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Successful Requests: {cb.successful_requests}")
        print(f"Total Cost (USD): ${cb.total_cost}")

    return response

url = "https://edition.cnn.com/2023/04/13/business/delta-earnings/index.html"
#summarize_docs(UnstructuredURLLoader(urls = [url]).load(), url)
urls = [
    "https://edition.cnn.com/2023/04/13/business/delta-earnings/index.html"
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://goo.gl/maps/NDSHwePEyaHMFGwh8",
]
summarize_docs(UnstructuredURLLoader(urls).load(), url)


# urls = [
#     "https://edition.cnn.com/2023/04/13/business/delta-earnings/index.html"
#     "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
#     "https://goo.gl/maps/NDSHwePEyaHMFGwh8",
# ]
# loader = SeleniumURLLoader(urls=urls)
# data = loader.load()
# summarize_docs(data, url)



