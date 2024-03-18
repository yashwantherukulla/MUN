from pydantic import BaseModel
class messages(BaseModel):
    messages: dict = {}
    host_code: str = "None"
    country_code: str = "None"

class sendMessages(BaseModel):
    message: dict = {}
    host_code: str = "None"
    country_code: str = "None"
    
class emailAdd(BaseModel):
    email: str = None

class munPage(BaseModel):
    email: str = ''