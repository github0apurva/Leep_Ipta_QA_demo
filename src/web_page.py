import os
from pathlib import Path

from src.constants import *
from src.utils import read_yaml, extract_links, write_list_as_txt

from dotenv import load_dotenv
load_dotenv(CUSTOM_ENV_NAME)

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_CSE_ID"] = os.getenv("GOOGLE_CSE_ID")

from langchain_community.utilities import GoogleSearchAPIWrapper


def extract_related_links ():
    """
    read context and number of results from params.yaml
    returns a text file with saved list of web pages to be vectorized
    """
    # extract the context and length of search for websites
    params = read_yaml(1, PARAMS_FILE_PATH)
    search_context = params['Web_page_search_context']
    search_num = params['number_of_pages']
    print (search_context, "for ", search_num, " pages")

    # use the context and length to do a google search using an api wrapper
    api_wrapper = GoogleSearchAPIWrapper( siterestrict = False )
    link_in_dict = api_wrapper.results (search_context  , search_num )
    print ( "Activity  2 : Done: getting webpages from Google wrapper")

    # Extract the links from the above dictionary to a list so as to be used for webbasedloader
    link_in_list =  extract_links( 3,  link_in_dict , 'link')

    # write the list in a txt file (always overwrites)
    write_list_as_txt ( 4, link_in_list )

    return 

