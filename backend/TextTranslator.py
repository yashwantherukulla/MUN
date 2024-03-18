from googletrans import Translator
from PyPDF2 import PdfReader

translator = Translator()

def translate(text:str, dest:str):
    response = translator.translate(text, dest=dest)
    return response.text


def pdf2txt(file_path):
    pdf = PdfReader(file_path)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text


def main(dest_lang:str, file_path):
    text = pdf2txt(file_path)
    translated_text = translate(text, dest_lang)
    return translated_text