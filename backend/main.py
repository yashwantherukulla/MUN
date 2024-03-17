from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
import asyncio

from Searcher import Searcher

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
                            The summary should be no longer than 3 sentences.
                            INPUT TEXT: {inputText}""")
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"inputText": text})
    return response

def create_search_qns(statement:str):

    SQprompt = PromptTemplate.from_template("""As an AI trained to generate questions, your task is to create a set of questions that delve deeper into a given topic. Your questions should guide the user towards the answers they seek and validate the statement given.

Please adhere to the following guidelines:
1) Do not repeat questions.
2) Ensure your questions are relevant to both the given question and context.
3) Generate a minimum of 1 and a maximum of 4 questions.
4) Your questions should explore the topic in depth, based on the given statement.
5) The output should be a list of questions.
6) The questions should be likely to be asked by a human, given the context and question.
7) The questions MUST be relevant to the statement.
8) Be specific to the given context in your questions.
9) Avoid vague language in your questions. Be specific and direct.

For example:
Given statement: "The international community must urgently collaborate to implement robust measures to mitigate climate change, including enforcing strict regulations on carbon emissions, accelerating the transition to renewable energy sources, investing in sustainable infrastructure, and fostering global cooperation through initiatives such as the Paris Agreement."
Output: ["How effective have previous international collaborations been in mitigating climate change, and what evidence supports this effectiveness?", "What evidence exists to demonstrate that accelerating the transition to renewable energy sources will significantly contribute to mitigating climate change?", "Are there contingency plans in place to address potential unforeseen challenges or obstacles in the implementation of these measures?", "How will progress be monitored and evaluated to ensure that the proposed measures are achieving their intended goals in mitigating climate change?"]

Now, let's generate questions for the given statement: {Statement}""")
    chain = SQprompt | llm | StrOutputParser()
    search_qns = chain.invoke({"Statement": statement})
    search_qns = search_qns.split("\n")
    # search_qns = [qn for qn in search_qns if qn]
    return search_qns

def semantic_sentence_splitter(input_text: str):
        prompt = PromptTemplate.from_template("""Given the input text, split the input text into sentences.
                                The sentences should be split semantically.
                                A sentence that is split must be a complete sentence making sense on its own without needing any prior context.
                                The input text is a string of words.
                                The output should be a list of sentences.
                                For example, if the input text is "Hello, how are you? I am fine.", the output should be ["Hello, how are you?", "I am fine."].
                                NOTE: the output MUST be a list of strings.
                                INPUT TEXT: {inputText}""")
        
        chain = prompt | llm | StrOutputParser()
        response = chain.invoke({"inputText": input_text})
        # response = response.split("\n")
        # response = [stmnt for stmnt in response if stmnt]
        return eval(response)


class FactAnalDS(BaseModel):
    isFactual: str = Field(description="tells if the statement is factual or not")
    reason: str = Field(description="reason why the statement is not factual, if it is not factual. If it is factual, then this field must be empty.")
    crct_stmnt: str = Field(description="corrected statement if the input statement is not factual")

async def fact_analyser(input_text: str):

    questions = create_search_qns(input_text)

    searcher = Searcher()
    reference_texts = []
    for question in questions:
        reference_text = await searcher.search_and_get_content(question)
        reference_texts.append(reference_text)
    
    parser = JsonOutputParser(pydantic_object=FactAnalDS)
    prompt = PromptTemplate.from_template("""Given the input text, see if the sentence is factual or not.
                            If it factual, then just return 'true' and reason as 'None'.
                            else (i.e., if it is not factual), then return 'false' and give a reason why it is not true with corrected statement in crct_stmnt field in the output. This reason must be under 100 words And the corrected statement should have similar length to the input statement.
                            NOTE: use your references to help you decide if the sentence is factual or not.
                            NOTE: do not imagine your own references, use the ones provided.
                            NOTE: If the sentence is factual, then the reason and crct_stmnt fields must be 'None' in the output.
                            NOTE: true, false, and None are case sensitive strings and must be given with quotation marks.
                            OUTPUT FORMAT: {outputFormat}

                            Here are the inputs you need,
                            INPUT TEXT: {inputText}
                            
                            To help you decide if the sentence is factual or not, you can use the following resources:
                            {referenceTexts}""")
    
    chain = prompt | llm | parser

    response = chain.invoke({"inputText": input_text, "referenceTexts": reference_texts, "outputFormat": parser.get_format_instructions()})
    
    return response

async def main(text:str):
    # split_text = semantic_sentence_splitter(text)
    tfJSON = {}
    split_text = text.split('.')
    
    for i,t in enumerate(split_text):
        out = await fact_analyser(t)
        tfJSON[i] = out


    tfJSON[i+1] = {'text_summ': summarize(text)}


    return tfJSON
        

        

text = "A comprehensive approach to promoting gender equality and empowering women in the workforce involves implementing legislation to guarantee equal pay for equal work, establishing accessible childcare services to facilitate women's participation in employment, providing training and educational opportunities to enhance women's skills and qualifications, and advancing women's representation in leadership roles through affirmative action policies."

print(asyncio.run(main(text)))