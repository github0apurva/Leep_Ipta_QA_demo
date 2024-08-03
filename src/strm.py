import streamlit as st
import time
from datetime import timedelta
from langchain.chains import create_retrieval_chain
from src.constants import *
from src.utils import read_yaml
from PIL import Image

def talk_to_stream (retrieval_chain):
    strt =  time.time()
    
    params = read_yaml(5, PARAMS_FILE_PATH)

    prompt_zero_shot = params['prompt_zero_shot']
    prompt_few_text1 = params['prompt_few_text_short']
    prompt_few_text2 = params['prompt_few_text_long']
    if prompt_zero_shot == True and prompt_few_text1 == "" and prompt_few_text2 == "":
        prompt_examples1 = ""
        prompt_examples2 = ""
    else :
        prompt_examples1 = "Few sample questions and answers seperated by | are as per below: " + prompt_few_text1
        prompt_examples2 = "Few sample questions and answers seperated by | are as per below: " + prompt_few_text2

    img = Image.open("Designer.png")
    st.image(img, width=150)

    st.title("Demo for Novartis")
    st.subheader("This is a Question answering system from selected webpages")
    
    print ("Activity ", 6, ": Done: Stream is ready")

    input_text = st.text_input ("Input the question you have about Iptacopan :")
    response_length_small = st.selectbox("Answer length: ",
                     ['Short', 'Long'])
    # prompt_text = ""
    # if response_length_small == 'Short':
    #     prompt_text = " Use three sentences maximum and keep the answer concise. "
    print ("Activity ", 7, ": Done: Stream got inputs")
    print ("within stream: Done with first step, time elpased: ", timedelta(seconds=time.time()-strt) )
    if(st.button("Get answer")) and  input_text: 
        st.markdown('''Response will take few minutes !!! :hourglass_flowing_sand:''')
        
        if response_length_small == 'Short':
            print ( " used short answer and ", prompt_examples1 )
            prompt_text = " Use four sentences maximum and keep the answer concise. "
            prompt_examples = prompt_examples1
        else:
            print ( " used long answer and ", prompt_examples2 )
            prompt_text = " Use ten sentences maximum and stick to facts. Answer with bullets points and be descriptive. "
            prompt_examples = prompt_examples2

        print ("within stream: Starting the response, time elpased: ", timedelta(seconds=time.time()-strt) )
        #response = retrieval_chain.invoke ({"input":input_text})
        print ("Activity ", 8, ": Invoke start")
        response = retrieval_chain.invoke ({"input":input_text, "prompt_text":prompt_text, "prompt_examples": prompt_examples })
        print ("within stream: Done with the response, time elpased: ", timedelta(seconds=time.time()-strt) )
        st.text_area(label = "Response" , value=response['answer'], height =500, label_visibility  = 'hidden')