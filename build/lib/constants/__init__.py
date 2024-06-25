from pathlib import Path
import os

PARAMS_FILE_PATH = Path ( "params.yaml")

CUSTOM_ENV_PATH = lambda a : '/'.join(os.get_exec_path()[0].split('\\')[:-2])+'/'+a
CUSTOM_ENV_NAME = CUSTOM_ENV_PATH('chatter.env')

WEB_PAGE_TXT  = "web_page.txt"


