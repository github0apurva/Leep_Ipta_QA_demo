


ask = input("Enter Y if need full run ( create new vector store), N if only Q&A (based on previously built Vectors) : ")


if ask.upper() == 'Y':
    from src.web_page import extract_related_links
    from src.vectdb import create_vector
    extract_related_links()
    create_vector()

