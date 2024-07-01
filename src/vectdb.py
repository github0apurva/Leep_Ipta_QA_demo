import yaml
from pathlib import Path 
import os

from src.constants import *
from src.utils import read_yaml, read_from_text, vectordb_write

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



import streamlit as st
import time

def create_vector ():
    """
    read chunk size and overlap from params.yaml
    """
    # read the list of webpage to be taken
    links_to_load = read_from_text ( 5, WEB_PAGE_TXT )
    #print ( links_to_load )
    # use a loader to get all content

    
    loader = WebBaseLoader(web_paths = links_to_load,)
                    #        bs_kwargs= dict(parse_only = bs4.SoupStrainer(
                    #        class_ = ("post-title","post-content","post-header")
                    #    )),)    

    web_docs = loader.load()
    print ("               size of the web docs : ",len(web_docs))
    print ("Activity ", 6, ": Done: webpage content from links")
    
    # extract the size and overlap chars from param file
    params = read_yaml(7, PARAMS_FILE_PATH)
    chunk_size = params['chunk_size']
    chunk_overlap = params['chunk_overlap']
    print ("               ", chunk_size, "is the chunk size choosen with ", chunk_overlap, " chars overlaps ")

    # splitting the docs based on above size etc
    documents = RecursiveCharacterTextSplitter(chunk_size = chunk_size, chunk_overlap = chunk_overlap).split_documents(web_docs)
    # taking only top n docs
    docs_to_vectorize_take = min ( params['docs_to_vectorize'] , len(web_docs))
    documents_filtered = documents[:docs_to_vectorize_take]
    print ("Activity ", 7, ": Done: documents ready & filtered")
    # choosing the embeddings to use
    embeddings_to_use = params['embeddings_to_use']
    if embeddings_to_use == "Instruct":
        choosen_embeddings = HuggingFaceInstructEmbeddings(model_name = 'hkunlp/instructor-xl',  
                                                   model_kwargs={"device":"cpu"},
                                                   encode_kwargs ={'normalize_embeddings': True} )
    else :
        choosen_embeddings = OllamaEmbeddings()
    # creatign vector store and eventually retreiver
    verctordb = FAISS.from_documents(documents_filtered, choosen_embeddings )
    print ("Activity ", 8, ": Done: vector db creation")
    #retriever = verctordb.as_retriever()
    vectordb_write ( 9, DB_FAISS_NM , os.getcwd() , verctordb )
    return 

