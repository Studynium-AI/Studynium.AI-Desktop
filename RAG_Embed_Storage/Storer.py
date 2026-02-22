import langchain_community.vectorstores
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pydantic import SecretStr


# import Chunker

def embedder():
    """
    creates an embeddings instance (embedding-001) and returns it
    :return: embeddings instance
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if api_key is None:
         raise ValueError("The GOOGLE_API_KEY environment variable is not set.")
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=SecretStr(api_key))

def metaWriter(chunked: list[Document]):
    """
    writes ids to chunks and adds it into the metadata in the form
    ./folder/PageSource:PageNumber:ChunkIndex
    e.g. ./data/file.pdf:0:4
    :param chunked: list of Chunked Documents
    :return: list of IDed Chunked Documents
    """
    lastPageID = None
    currChunkIndex = 0
    # Page Source : Page Number : Chunk Index
    for chunk in chunked:
        print(f"current_chunk_index: {currChunkIndex}, lastPageID: {lastPageID}")
        currSource = chunk.metadata.get('source')
        currPage = chunk.metadata.get('page')
        currentPageID = f"{currSource}:{currPage}"
        if lastPageID == currentPageID:
            currChunkIndex += 1
            #increment the index for the same page
        else:
            currChunkIndex = 0
            # reset the index everytime we encounter a new page

        chunkID = f"{currentPageID}:{currChunkIndex}"
        lastPageID = currentPageID
        chunk.metadata["id"] = chunkID

    return chunked

#todo: try to add a smart deleter that deletes files from the vector DB

def Storer(IDedChunks: list[Document]):
    """
    takes in a list of IDed Chunked Documents and stores/updates
    them in the form of a Chroma Vector DB file/folder.
    :param IDedChunks: list of IDed Chunked Documents
    :return: True -> committed successfully False -> not committed successfully
    """
    # takes the IDed chunks from the metaWriter
    try:
        db = langchain_community.vectorstores.Chroma(
            persist_directory="./VectorDBFiles",embedding_function=embedder()
        )

        # check for existing files:
        existingChunks = db.get(include=[])
        existingIDs = set(existingChunks["ids"])
        print(f"No of existing chunks: {len(existingIDs)}")

        newChunks = []
        for chunk in IDedChunks:
            if chunk.metadata["id"] not in existingIDs:
                newChunks.append(chunk)
            #debugging
            print(f"Adding chunk of id: {chunk.metadata['id']}")
            print(f"chunk: {chunk}")

        if len(newChunks):
            print(f"Storing Documents (Chunks): {len(newChunks)}")
            newChunkIds = [chunk.metadata["id"] for chunk in newChunks]
            db.add_documents(newChunks, ids=newChunkIds)
            db.persist() # automatically persisted but used for good measure
        else:
            print("No new Documents found")

        return True
    except Exception as e:
        return False
