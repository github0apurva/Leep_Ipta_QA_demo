import warnings
warnings.filterwarnings("ignore")
import time
from datetime import timedelta

ask = input("Enter Y if need full run ( create new vector store), N if only Q&A (based on previously built Vectors) : ")


if ask.upper() == 'Y':
    start = time.time()
    print ("Started working on vectors, time elpased: ", timedelta(seconds=time.time()-start) )
    from src.web_page import extract_related_links
    from src.vectdb import create_vector
    extract_related_links()
    create_vector()
    print("time elpased: ", timedelta(seconds=time.time()-start) )

