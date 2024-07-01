Web_page_search_context = "novartis Iptacopan competitors"
number_of_pages = 2
chunk_size = 1000
chunk_overlap =20
docs_to_vectorize = 1000
embeddings_to_use ='Ollama'
model_to_use = 'Ollama'

from pathlib import Path
import os
import yaml
from pathlib import Path 
from box.exceptions import BoxValueError
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.utilities import GoogleSearchAPIWrapper

CUSTOM_ENV_PATH = lambda a : '/'.join(os.get_exec_path()[0].split('\\')[:-2])+'/'+a
CUSTOM_ENV_NAME = CUSTOM_ENV_PATH('chatter.env')

load_dotenv(CUSTOM_ENV_NAME)



os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_CSE_ID"] = os.getenv("GOOGLE_CSE_ID")


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


#functions
def extract_links ( ac, link_in_dict, dict_key ='link' ):
    """
    reads a list of dictionaries and returns specific value for a key 
    """
    link_in_list = [ link_in_dict[i][dict_key] for i in range(len(link_in_dict)) ]
    print ( "Activity ", ac, ": Done: extracting webpage from dict")
    return link_in_list

def extract_related_links ():
    """
    read context and number of results from params.yaml
    returns a text file with saved list of web pages to be vectorized
    """
    # extract the context and length of search for websites
    search_context =Web_page_search_context
    search_num = number_of_pages
    print (search_context, "for ", search_num, " pages")

    # use the context and length to do a google search using an api wrapper
    api_wrapper = GoogleSearchAPIWrapper( siterestrict = False )
    link_in_dict = api_wrapper.results (search_context  , search_num )
    print ( "Activity 2: Done: getting webpages from Google wrapper")
    # Extract the links from the above dictionary to a list so as to be used for webbasedloader
    link_in_list =  extract_links( 3,  link_in_dict , 'link')

    return link_in_list



def create_vector (links_to_load):
    """
    read chunk size and overlap from params.yaml
    """
    # # read the list of webpage to be taken
    # links_to_load = read_from_text ( 5, WEB_PAGE_TXT )

    # use a loader to get all content
    loader = WebBaseLoader(web_paths = links_to_load,)
                    #        bs_kwargs= dict(parse_only = bs4.SoupStrainer(
                    #        class_ = ("post-title","post-content","post-header")
                    #    )),)    
    web_docs = loader.load()
    print ("size of the web docs : ",len(web_docs))
    print ("Activity ", 6, ": Done: webpage content from links")
    
    # extract the size and overlap chars from param file
    print (chunk_size, "is the chunk size choosen with ", chunk_overlap, " chars overlaps ")

    # splitting the docs based on above size etc
    documents = RecursiveCharacterTextSplitter(chunk_size = chunk_size, chunk_overlap = chunk_overlap).split_documents(web_docs)
    # taking only top n docs
    docs_to_vectorize_take = min ( docs_to_vectorize, len(web_docs))
    documents_filtered = documents[:docs_to_vectorize_take]
    # choosing the embeddings to use
    if embeddings_to_use == "Instruct":
        print ( "Instruct Embeddings" )
        choosen_embeddings = HuggingFaceInstructEmbeddings(model_name = 'hkunlp/instructor-xl',  
                                                   model_kwargs={"device":"cpu"},
                                                   encode_kwargs ={'normalize_embeddings': True} )
    else :
        choosen_embeddings = OllamaEmbeddings()
        print ( "Ollama Embeddings" )
    # creatign vector store and eventually retreiver
    verctordb = FAISS.from_documents(documents_filtered, choosen_embeddings )
    #retriever = verctordb.as_retriever()
    return verctordb, choosen_embeddings

def vectordb_write ( index_name, path, my_vector ):
    my_vector.save_local ( path , index_name )
    print ("Activity  : Done: Vector DB saved to disk")
    return

def vectordb_read ( my_index_name, path, my_embeddings ):
    my_vector = FAISS.load_local ( path, index_name  = my_index_name,
                               embeddings = my_embeddings , allow_dangerous_deserialization = True   ) 
    return my_vector



def get_retrieval_chain (retriever):
    # get prompt
    # prompt = hub.pull("hwchase17/openai-functions-agent")
    # print( prompt.messages )
    prompt = ChatPromptTemplate.from_template(
    """
    You are an assistant for question-answering tasks. Use the provided context only to answer the question. 
    {prompt_examples}
    If you don't know the answer, just say that you don't know. {prompt_text}
    Please provide the most accurate response based on the question.
    <context>
    {context}
    <context>
    Questions: {input}
    """)

    #llm = Ollama(model = "llama2")
    llm= ChatOllama(model="llama2")

    # creating document chain
    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain (retriever, document_chain)
    return retrieval_chain

def talk_to_stream (retrieval_chain):
    prompt_text = " Use three sentences maximum and keep the answer concise. "
    prompt_few_text = """ "Input":"where was Iptacopan discovered?", "Output": "iscovered at the Novartis Biomedical Research, iptacopan is currently in development for a range of complement-mediated diseases including paroxysmal nocturnal hemoglobinuria (PNH), immunoglobulin A nephropathy (IgAN), C3 glomerulopathy (C3G), immune complex membranoproliferative glomerulonephritis (IC-MPGN) and atypical hemolytic uremic syndrome (aHUS)", 
    "Input":"How does Iptacopan compares with Soliris", "Output": "Iptacopan was compared to AstraZeneca/Alexion’s Soliris (eculizumab) and Ultomiris (ravulizumab). Both drugs are anti-complement component 5 (C5) monoclonal antibodies, approved for PNH and atypical hemolytic uremic syndrome, generalized myasthenia gravis and neuromyelitis optica spectrum disorder"."""
    prompt_examples = "Few sample questions and answers are " + prompt_few_text


    st.title("Demo with LLAMA2")

    input_text = st.text_input ("Input the question you have about Iptacopan ")
    #input_text = "what is Iptacopan"
    if input_text:
        start_time = time.process_time()
        #response = retrieval_chain.invoke ({"input":input_text})
        response = retrieval_chain.invoke ({"input":input_text, "prompt_text":prompt_text, "prompt_examples": prompt_examples })
        print ("response time: ",time.process_time()-start_time)
        print ( response['answer'] )
        st.write(response['answer'])





print ( "Done Reading" )

list_link = extract_related_links()
print ( "Done Reading 1" )

my_vector , my_embeddings = create_vector (list_link  )
vectordb_write ( 'nova_vector_db', os.getcwd() , my_vector )
loaded_vector = vectordb_read ( 'nova_vector_db', os.getcwd(), my_embeddings )
retr = loaded_vector.as_retriever()
#retr = create_retreiver (list_link)
print ( "Done Reading 2" )
rc  = get_retrieval_chain (retr)
print ( "Done Reading 3" )
talk_to_stream ( rc )

