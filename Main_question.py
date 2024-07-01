
from src.retrvl_chain import get_retrieval_chain
from src.strm import talk_to_stream

import warnings
warnings.filterwarnings("ignore")

ret_ch = get_retrieval_chain()
talk_to_stream ( ret_ch ) 