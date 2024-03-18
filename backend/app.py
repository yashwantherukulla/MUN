
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
from backend.database import *

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
from fastapi.responses import RedirectResponse
    
service_account_key_file = "backend/FirebaseServiceAccountKey.json"

app = FastAPI()

firebase_admin.initialize_app(options={
    'credential': firebase_admin.credentials.Certificate(service_account_key_file)
})

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = auth.verify_id_token(token)
        uid = payload.get('uid')
        if uid is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
)




# Add the CORS middleware to your FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],
)


@app.post("/verify-token")
async def verify_token(id_token: str):
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        return {"uid": uid}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid token")
        

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
async def get_messagesL(data: messages, current_user: dict = Depends(get_current_user)):
    host_code = data.host_code
    country_code = data.country_code
    data = {'host_code': host_code, 'country_code': country_code}

@app.post('/send_message')
async def send_message(data: sendMessages):
    pass

