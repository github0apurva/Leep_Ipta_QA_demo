import streamlit as st
import time
from langchain.chains import create_retrieval_chain


def talk_to_stream (retrieval_chain):
    st.title("Demo with LLAMA2")

    input_text = st.text_input ("Input the question you have about Iptacopan ")
    
    if input_text:
        start_time = time.process_time()
        response = retrieval_chain.invoke ({"input":input_text})
        print ("response time: ",time.process_time()-start_time)
        st.write(response['answer'])