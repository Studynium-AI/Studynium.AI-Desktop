import re
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
# from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from RAG_Embed_Storage import Storer
import google.generativeai as genai

def removeThinkTags(text: str) -> str:
    cleaned_text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    cleaned_text = cleaned_text.strip()
    return cleaned_text
'''
def extractAnswersNSuggestions(text: str) -> tuple:
    pattern = r"answers:"
    regex = re.findall()
    return (answer,search)
'''
def RAGen(prompt: str,modelInfo: int=0) -> str:
    # Storer.get_embedding_model()  # Initialize the google generative ai model
    # db = Chroma(persist_directory="./VectorDBFiles")
    # prompt = "What is document 3 about?"
    # # We still use similarity_search (NOT similarity_search_with_score)
    # #  because we provided embeddings directly.
    # result = db.similarity_search(prompt, k=5)
    db = Chroma(persist_directory="./VectorDBFiles",embedding_function=Storer.embedder())
    result = db.similarity_search_with_score(prompt,k=8)
    context = "\n\n---\n\n".join([doc.page_content for doc, _score in result])
    RAGPrompt = f"""you are a helpful ai assistant aimed at providing the most accurate and correct information.
                    answer the following 90% of the question based on the context below. 
                    you are allowed to use some known data from your training set.
                    you have to explain it in 200-300 words if possible. you may use analogies if needed.
                    try to be descriptive enough for a 12th grade student to understand the concept clearly.

                    context :
                    {context}
                    
                    question :
                    {prompt} 
                    
                    also create 5 search suggestions to search in a web browser for the 
                    user to gain more information about the question. you may use the Contexts to get more information.
                    format the answer by giving a answer in the format. do not hallucinate links!!!
                    answer : [<contents of answer>]
                    searches : [<recommended searches as a numbered list>]
                    """
    print(RAGPrompt)
    if modelInfo == 1:
        ollamaMod = Ollama(model="deepseek-r1:8b",temperature=0.3)
        answer = ollamaMod.invoke(RAGPrompt)
        answer =removeThinkTags(answer)
    elif modelInfo == 2:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if api_key is None:
            raise ValueError("The GOOGLE_API_KEY environment variable is not set.")
        genai.configure(api_key=api_key)
        generation_config = genai.GenerationConfig(
        temperature=0.3,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        )
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=generation_config
            # safety_settings = Adjust safety settings
            # See https://ai.google.dev/gemini-api/docs/safety-settings
        )
        answer = model.generate_content(RAGPrompt)
    else :
        ollamaMod = Ollama(model="deepseek-r1:1.5b",temperature=0.5)
        answer = ollamaMod.invoke(RAGPrompt)
        answer =removeThinkTags(answer)
    sources = [doc.metadata.get("id", None) for doc, _score in result]
    # answer,searchRecommendations = extractAnswersNSuggestions(answer)
    # return answer, sources, searchRecommendations
    formattedResponse = f"Response: {answer}\nSources: {sources}"
    return formattedResponse
