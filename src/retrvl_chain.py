
from pathlib import Path 
import os

from src.constants import *
from src.utils import read_yaml, vectordb_read

from dotenv import load_dotenv
load_dotenv(CUSTOM_ENV_NAME)


from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from InstructorEmbedding import INSTRUCTOR
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain import hub
from langchain_community.chat_models import ChatOllama
from langchain_community.llms import Ollama
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain



def get_retrieval_chain ():
    params = read_yaml(1, PARAMS_FILE_PATH)
    # choosing the embeddings to use
    embeddings_to_use = params['embeddings_to_use']
    if embeddings_to_use == "Instruct":
        choosen_embeddings = HuggingFaceInstructEmbeddings(model_name = 'hkunlp/instructor-xl',  
                                                   model_kwargs={"device":"cpu"},
                                                   encode_kwargs ={'normalize_embeddings': True} )
    else :
        choosen_embeddings = OllamaEmbeddings()

    # get prompt
    # prompt = hub.pull("hwchase17/openai-functions-agent")
    # print( prompt.messages )

    #prompt_style_to_use
    prompt = ChatPromptTemplate.from_template(
    """
    You are an assistant for question-answering tasks. Use the provided context only to answer the question. 
    {prompt_examples}
    If you don't know the answer, just say that you don't know. {prompt_text}
    Use the provided context only to answer the question. Please provide the most accurate response based on the question.
    <context>
    {context}
    <context>
    Questions: {input}
    """)
    #llm = Ollama(model = "llama2")
    llm= ChatOllama(model="llama2")
    #llm= ChatOllama(model="llama2", top_k = 10 , temperature = 0.2 , num_gpu = 1 )
    print ("Activity ", 2, ": Done: Prompt template and LLM ready")
    loaded_vector = vectordb_read ( 3, DB_FAISS_NM, os.getcwd(), choosen_embeddings )
    retriever = loaded_vector.as_retriever()

    # creating document chain
    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain (retriever, document_chain)
    print ("Activity ", 4, ": Done: retrieval chain is ready")
    return retrieval_chain

