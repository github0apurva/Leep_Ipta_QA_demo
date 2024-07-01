from src.constants import *
from src.utils import read_yaml


params = read_yaml(7, PARAMS_FILE_PATH)

prompt_zero_shot = params['prompt_zero_shot']
prompt_few_text = params['prompt_few_text']
if prompt_zero_shot == True and prompt_few_text == "" :
    prompt_examples = "nothing"
else :
    prompt_examples = "Few sample questions and answers seperated by | are as per below: " + prompt_few_text

print ( prompt_examples )