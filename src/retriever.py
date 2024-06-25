import yaml
from pathlib import Path 
import os

from src.constants import *
from src.utils import read_yaml, read_from_text

from dotenv import load_dotenv
load_dotenv(CUSTOM_ENV_NAME)

from langchain_community.document_loaders import WebBaseLoader
import bs4
from langchain_text_splitters import RecursiveCharacterTextSplitter


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

import streamlit as st
import time

def create_retreiver ():
    """
    read chunk size and overlap from params.yaml
    """
    # read the list of webpage to be taken
    links_to_load = read_from_text ( 5, WEB_PAGE_TXT )

    # use a loader to get all content
    loader = WebBaseLoader(web_paths = links_to_load,
                           bs_kwargs= dict(parse_only = bs4.SoupStrainer(
                           class_ = ("post-title","post-content","post-header")
                       )),)    
    web_docs = loader.load()
    print ("size of the web docs : ",len(web_docs))
    print ("Activity ", 6, ": Done: webpage content from links")
    
    # extract the size and overlap chars from param file
    params = read_yaml(7, PARAMS_FILE_PATH)
    chunk_size = params['chunk_size']
    chunk_overlap = params['chunk_overlap']
    print (chunk_size, "is the chunk size choosen with ", chunk_overlap, " chars overlaps ")

    # splitting the docs based on above size etc
    documents = RecursiveCharacterTextSplitter(chunk_size = chunk_size, chunk_overlap = chunk_overlap).split_documents(web_docs)
    # taking only top n docs
    docs_to_vectorize = params['docs_to_vectorize']
    documents_filtered = documents[:docs_to_vectorize]
    # choosing the embeddings to use
    embeddings_to_use = params['embeddings_to_use']
    if embeddings_to_use == "Instruct":
        embeddings = HuggingFaceInstructEmbeddings(model_name = 'hkunlp/instructor-xl',  
                                                   model_kwargs={"device":"cpu"},
                                                   encode_kwargs ={'normalize_embeddings': True} )
    else :
        embeddings = OllamaEmbeddings()
    # creatign vector store and eventually retreiver
    verctordb = FAISS.from_documents(documents_filtered, embeddings )
    retriever = verctordb.as_retriever()
    return retriever

def create_retrieval_chain (retriever):
    # get prompt
    prompt = hub.pull("hwchase17/openai-functions-agent")
    print( prompt.messages )

    #llm = Ollama(model = "llama2")
    llm= ChatOllama(model="llama2")

    # creating document chain
    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain (retriever, document_chain)
    return retrieval_chain

def talk_to_stream (retrieval_chain):
    st.title("Demo with LLAMA2")

    input_text = st.text_input ("Input the question you have about Iptacopan ")
    
    if input_text:
        start_time = time.process_time()
        response = retrieval_chain.invoke ({"input":input_text})
        st.write(response['answer'])