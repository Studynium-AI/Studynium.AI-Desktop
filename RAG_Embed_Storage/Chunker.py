from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.chains.retrieval_qa.base import RetrievalQA

#definitions
PDF_LOC = "./RAG_Embed_Storage/Files"

def loading():
    loader = PyPDFDirectoryLoader(PDF_LOC)
    print("loading")
    return loader.load()

def chunker(chunkable:list[Document]):
    """
    the  function takes in a document chunkable and returns a chunked list of document objects
    :param chunkable: list of document objects
    :return: list of document objects
    """
    textSplitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        # length_function=len,
        # is_separator_regex=False,
        #seperators and length_function are default
    )
    print("chunking")
    return textSplitter.split_documents(chunkable)