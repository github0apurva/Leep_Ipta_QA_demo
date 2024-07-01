import streamlit as st
from PIL import Image

img = Image.open("Designer.png")
st.image(img, width=200)

st.title("Demo for Novartis")
st.subheader("This is a Question answering system from selected webpages")





input_text = st.text_input ("Input the question you have about Iptacopan :")
hobby = st.selectbox("Answer length: ",
                     ['Short', 'Long'])
if(st.button("Get answer")) and  input_text: 
    st.markdown('''Response will take few minutes !!! :hourglass_flowing_sand:''')
    if hobby == 'Short':
        st.text_area(label = "" , value="perfect short", height =100)
    else: 
        st.write('perfect Long')
