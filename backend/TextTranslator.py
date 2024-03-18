from googletrans import Translator


translator = Translator()

def translate(text:str, dest:str):
    response = translator.translate(text, dest=dest)
    return response.text