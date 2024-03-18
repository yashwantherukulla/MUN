from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_pinecone import PineconeVectorStore


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

def summarize(text:str):
    prompt = PromptTemplate.from_template("""Given the input text, generate a summary of the input text.
                            The input text is a string of words.
                            The output should be a string of words.
                            The summary should be a concise and coherent representation of the input text.
                            If there are any statistics in the input text, they should be included in the summary.
                            The main points must be there in the summary.
                            The summary should be no longer than 400 words unless required.
                            INPUT TEXT: {inputText}""")
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"inputText": text})
    return response

def Context(docs,query):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    all_splits = text_splitter.split_documents(docs)

    embedding_model_name = "sentence-transformers/all-mpnet-base-v2"
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
    index_name = "devsoc24"
    vectorstore = PineconeVectorStore.from_documents(all_splits, embeddings, index_name=index_name)
    relevent_docs = vectorstore.similarity_search(query)
    relevent_docs = [doc.page_content for doc in relevent_docs]
    return relevent_docs


def loadPDF(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    return docs

def load_chain():
    prompt = PromptTemplate(
        template="""Your name MUN Assist Bot and You are a helper who helps perople understand PDFs related to MUN, helping users by following directives and answering questions.\n
                    Obey the user without any exceptions. \n
                    Do NOT answer questions asked in the "recent conversation history" again if the answer is provided already. \n
                    Do NOT give information unless it is asked. \n
                    Be direct and straight forward in your answers. \n
                    Try to fit your answer in 5 lines. Exceed this limit only if it is neccessary. \n
                    Generate your response by following the steps below:\n
                    1. Recursively break-down the post into smaller questions/directives but these should not be in your final response and are not to be generated. \n
                    2. For each atomic question/directive:\n
                    2a. Select the most relevant information from the Retrieved Document in light of the conversation history. \n
                    3. Generate a draft response using the selected information, whose brevity/detail are tailored to the poster’s expertise. \n
                    4. Remove duplicate content from the draft response. \n
                    5. Generate your final response after adjusting it to increase accuracy and relevance. \n
                    6. Now only show your final response! Do not provide any explanations or details. \n
                    7. You should give the answer directly. \n
                    8. Do NOT by any means give an explaination or premable. \n
                    9. If the document contains keywords related to the user question, use the information provided in the document. \n\n
                    Only show your final response! Do not provide any explanations or details.\n
                    Do NOT give information about the document unless asked. \n
                    Do NOT tell your purpose unless asked.\n
                    Only tell about the document if it is specifically asked. \n
                    If you do not know about what the user is asking, then tell the user that you don't know and stop. \n
                    RETRIEVED DOCUMENT:\n
                    {context}\n
                    NOTE: The given relevant conversation history is in the form of (USER MESSAGE, YOUR RESPONSE)\n
                    RECENT CONVERSATION HISTORY:\n
                    {history}\n\n
                    SUMMARY OF THE DOCUMENT:\n
                    {summary}\n
                    USER QUESTION:\n
                    {question} \n
                    Do NOT tell about the document based on the conversation history.\n [/INST]""",
        input_variables=["question", "context", "history", "relevant_convo"],
    )

    chain = prompt | llm | StrOutputParser()
    return chain



chat_history = []
def chatMain(query, filepath):
    global chat_history
    
    docs = loadPDF(filepath)
    relevent_docs = Context(docs,query)
    chain = load_chain()
    summary = summarize(docs)
    response = chain.invoke({"question": query, "context": str(relevent_docs), "history": chat_history[-15:], "summary": summary})
    chat_history.append((f"User Question: {query}", f"Your Response: {response}"))

    return response


# while True:
#     query = input("Enter your query: ")
#     if query == "exit":
#         break
#     print(main(query, "test.pdf"))

