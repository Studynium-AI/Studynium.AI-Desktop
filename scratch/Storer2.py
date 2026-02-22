#import os
from typing import List
import google.generativeai as genai
#from langchain_chroma import Chroma
import chromadb
from langchain_core.documents import Document
#from dotenv import load_dotenv

#load_dotenv()  # Load environment variables from .env

#todo: https://docs.trychroma.com/docs/collections/update-data
#todo: https://docs.trychroma.com/docs/collections/add-data

def get_embedding_model():
    """
    Configures the google.generativeai library with the API key.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if api_key is None:
         raise ValueError("The GOOGLE_API_KEY environment variable is not set.")
    genai.configure(api_key=api_key)


def metaWriter(chunked_docs: List[Document]) -> List[Document]:
    """
    Adds unique IDs to the metadata of each chunked document.
    The ID format is: ./folder/PageSource:PageNumber:ChunkIndex
    e.g., ./data/file.pdf:0:4

    Args:
        chunked_docs: A list of chunked Documents.

    Returns:
        List[Document]: A list of IDed chunked Documents.
    """
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunked_docs:
        current_source = chunk.metadata.get('source')
        current_page = chunk.metadata.get('page')
        current_page_id = f"{current_source}:{current_page}"

        if last_page_id == current_page_id:
            current_chunk_index += 1  # Increment index for the same page
        else:
            current_chunk_index = 0  # Reset index for a new page

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id
        chunk.metadata["id"] = chunk_id

    return chunked_docs

def Storer(IDedChunks: List[Document]) -> bool:
    """
    Stores/updates IDed chunked documents in a Chroma Vector DB
    using google.generativeai's embed_content.

    Args:
        IDedChunks: A list of IDed chunked Documents.

    Returns:
        bool: True if committed successfully, False otherwise.
    """
    try:
        client = chromadb.Client()
        get_embedding_model()  # Configure the google.generativeai library

        collection = client.cr(persist_directory="./VectorDBFiles")

        existingChunks = collection.get(include=[])
        existingIDs = set(existingChunks["ids"])
        print(f"No of existing chunks: {len(existingIDs)}")

        newChunks = []
        for chunk in IDedChunks:
            if chunk.metadata["id"] not in existingIDs:
                newChunks.append(chunk)

        if newChunks:
            print(f"Storing Documents (Chunks): {len(newChunks)}")
            texts = [chunk.page_content for chunk in newChunks]
            metadatas = [chunk.metadata for chunk in newChunks]
            ids = [chunk.metadata["id"] for chunk in newChunks]

            # Batch embedding using genai.embed_content
            embeddings = []
            batch_size = 5  # Process in batches (adjust as needed)
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                result = genai.embed_content(
                    model="models/text-embedding-004",
                    content=batch,
                )
                embeddings.extend(result["embedding"]) #result is a dict

            collection.add_texts(texts=texts, embeddings=embeddings, metadatas=metadatas, ids=ids)
        else:
            print("No new Documents found")

        return True
    except Exception as e:
        print(f"Error during storing: {e}")
        return False
