import yaml
from pathlib import Path 
from box.exceptions import BoxValueError
from src.constants import *

def read_yaml (ac, path_yaml:Path) :
    """
    reads yaml file and returns it
    """
    try:
        with open(path_yaml,'r') as f:
            content = yaml.safe_load(f)
            print ( "Activity ", ac, ": Done: reading yaml file")
            return (content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    

def extract_links ( ac, link_in_dict, dict_key ='link' ):
    """
    reads a list of dictionaries and returns specific value for a key 
    """
    link_in_list = [ link_in_dict[i][dict_key] for i in range(len(link_in_dict)) ]
    print ( "Activity ", ac, ": Done: extracting webpage from dict")
    return link_in_list

def write_list_as_txt ( ac, list_to_print ):
    """
    takes in a list and prints in the text file provided through constants
    """
    if ( not os.path.exists( WEB_PAGE_TXT) ) or  (os.path.getsize(WEB_PAGE_TXT)== 0 ) :
        print ( "               txt status: file is empty or dont exists")
    else:
        print ( "              txt status: file already exists, overwriting it ")
    with open(WEB_PAGE_TXT, "w") as f:
        for line in list_to_print:
            f.write(f"{line}\n")
        f.close
        print ( "Activity ", ac, ": Done: writing webpage links to txt")
    return 


def read_from_text (ac, fle ):
    """
    reads the text file and sends as list
    """
    my_fle = open(fle, "r") 
    my_lst = my_fle.read().split("\n")
    print ( "Activity ", ac, ": Done: reading webpage from text file")
    return my_lst