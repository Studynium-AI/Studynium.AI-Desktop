from Generator_Runtime import Generator
from RAG_Embed_Storage.Chunker import *
from RAG_Embed_Storage.Storer import *
import warnings
#import fastapi

warnings.filterwarnings("ignore")

def main(action:str,prompt:str,modelInfo:int):
    while True:
        answer = ""
        sources = ""
        # action = input("What would you like to do? \n1.generate \n2.update \n3.exit \n\t🤨👉🏻")
        if action.lower() in ("generate", "1"):
            # prompt = input("What do you want to be clarified in??\n\t👨🏻‍🏫👉🏻")
            # try:
            #     modelInfo = int(input("Who do you want to be taught by\n1.Deepseek-r1 Pro \n2.Gemini Pro \n(any no).Deepseek-r1 ??\n\t👨🏻‍🏫👉🏻"))
            # except:
            #     modelInfo = 0
            answer = Generator.RAGen(prompt=prompt,modelInfo=modelInfo)
            print(f"Well i Think This is the answer you are looking for 🤓:\n{answer}")
            status = "generated successfully 🔥"
            break
        elif action.lower() in ("update", "2"):
            print("updating!!!!")
            chunkable = loading()
            # print(chunkable)
            chunked = chunker(chunkable)
            # print(chunked)
            IDedChunks = metaWriter(chunked)
            status = Storer(IDedChunks)
            if status:
                status = "Success 🥳"
            else :
                status = "Failed 😭"
            break
        else:
            status = "oops no such command found. Try again"
            # print("oops no such command found. Try again")

        return {"answer":answer[0], "status": status, "sources":answer[1], "searchRecommendations":answer[2]}
    #print(answer,"\n",status)

if __name__ == "__main__" :
     main(action="1",prompt="Tell me more on waves and how they travel",modelInfo=0)