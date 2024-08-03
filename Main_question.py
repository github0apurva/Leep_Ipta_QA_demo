
from src.retrvl_chain import get_retrieval_chain
from src.strm import talk_to_stream
import time
from datetime import timedelta
import warnings
warnings.filterwarnings("ignore")

start = time.time()
ret_ch = get_retrieval_chain()
print ("Done with first step, time elpased: ", timedelta(seconds=time.time()-start) )

talk_to_stream ( ret_ch ) 
print ("Done with second step, time elpased: ", timedelta(seconds=time.time()-start) )