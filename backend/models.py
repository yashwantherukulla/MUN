from pydantic import BaseModel

point_list=['General','Substantive Chit','Point of Enquiry','Point Of Information','Point Of Personal Privilege',"Point Of Order"]
all_opt='----All----'

class messages(BaseModel):
    messages: dict = {}
    host_code: str = "None"
    country_code: str = "None"
    email: str = ""
    
class messagesSRT(BaseModel):
    messages: dict = {}
    host_code: str = "None"
    country_code: str = "None"
    email: str = ""
    country: str = ""
    query: str = ""

class sendMessages(BaseModel):
    message: dict = {}
    host_code: str = "None"
    email: str = ""
    
class emailAdd(BaseModel):
    email: str = None

class munPage(BaseModel):
    email: str = ''
    
class munReg(BaseModel):
    email: str = ''
    host_code: str = ''