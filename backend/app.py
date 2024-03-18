
from fastapi import FastAPI, HTTPException, Depends, status
import firebase_admin
from firebase_admin import auth
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware  # Import the CORS middleware
import requests
import asyncio
import httpx
import logging
import json
from database import *
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
from fastapi.responses import RedirectResponse
from fastapi import Request
app = FastAPI()









# Add the CORS middleware to your FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],
)


@app.post('/get_messages')
async def get_messages(data: messages):
    host_code = data.host_code
    country_code = data.country_code
    data = {'host_code': host_code, 'country_code': country_code}
    async with httpx.AsyncClient() as client:
        response = await client.post('http://127.0.0.1:5000/confi', json=data)
    json_response = response.json()
    return {'messages': json_response}


@app.post('/get_messagesL')
async def get_messagesL(data: messages):
    host_code = data.host_code
    country_code = data.country_code
    data = {'host_code': host_code, 'country_code': country_code}

@app.post('/send_message')
async def send_message(data: sendMessages):
    
    pass



@app.post('/email_sign_up')
async def email_add(data: emailAdd, request: Request):
    try:
        email = data.email
        if "@" not in email:
            return {"status":"Failed"}
        #request.session["person"] = email 
        add_email(email)
        return {"status":"Success"}
    except:
        return {"status":"Failed"}


@app.post('/mun_page')
async def mun_page(data: munPage):
    person1 = session.query(Person).filter_by(email=data.email).first()#harshdipashah@gmail.com
    logging.info(data)
    user_mun = session.query(User).filter_by(person=person1.email).all()
    user_mun_list = []
    for i in user_mun:
        user_mun_list.append([i.host_code, session.query(Sw).filter_by(host_code=i.host_code).first().host_name])
    user_mun_reg = session.query(Sw).all()
    user_mun_reg_list = []
    for i in user_mun_reg:
        if [i.host_code, i.host_name] not in user_mun_list:
            user_mun_reg_list.append([i.host_code, i.host_name])
    return {"mun_list_user": user_mun_list, "mun_list_reg": user_mun_reg_list}
