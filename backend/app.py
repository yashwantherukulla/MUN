
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

def r(lst):
    lst.reverse()
    return lst







# Add the CORS middleware to your FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],
)


@app.post('/get_messages')
async def get_messages(data: messages):
    confi_srt= False
    if not data:
            return {'status': 'No input data provided'}, 400
    host_code = data.host_code
    email = data.email
    country_code = ''
    msg_data_rec=''
    msg_data_sent=''
    msg_data_eb=''
    eb=False
    country_list = sorted(country_li(host_code))
    try:
        user = session.query(User).filter_by(person=email, host_code=host_code).first()
        
        if user:
            country_code = user.post
            msg_data_rec=r(msg_rec(host_code,email))
            msg_data_sent=r(msg_sent(host_code,email))
            country_list.remove(user.post)
            if user.post.lower() == 'eb':
                eb=True
                msg_data_eb=r(msg_eb(host_code))
    except:
        pass
            
    return ({
    'point_list': point_list,
    'all_opt': all_opt,
    'confi_srt': confi_srt,
    'auto_r': True,
    'chits': swit(host_code),
    'h_c': False,
    'usr_country': country_code,
    'country_list': country_list,
    'msg_data_eb': msg_data_eb,
    'eb': eb,
    'msg_data_sent': msg_data_sent,
    'msg_data_rec': msg_data_rec,
    'title': 'Committee'
})


@app.post('/get_messages_sort')
async def get_messagesL(data: messagesSRT):
    confi_srt= True
    sort_country_q=data.country
    sort_query_q=data.query
    if not data:
            return {'status': 'No input data provided'}, 400
    host_code = data.host_code
    email = data.email
    country_code = ''
    msg_data_rec=''
    msg_data_sent=''
    msg_data_eb=''
    eb=False
    country_list = sorted(country_li(host_code))
    try:
        user = session.query(User).filter_by(person=email, host_code=host_code).first()
        country_code = user.post
        msg_data_rec=r(msg_sort_r(host_code,email,sort_country_q,sort_query_q))
        msg_data_sent=r(msg_sort_s(host_code,email,sort_country_q,sort_query_q))
        if user:
            country_list.remove(user.post)
            if user.post.lower() == 'eb':
                eb=True
                msg_data_eb=r(msg_eb(host_code))
    except:
        pass
            
    return ({
    'point_list': point_list,
    'all_opt': all_opt,
    'confi_srt': confi_srt,
    'auto_r': True,
    'chits': swit(host_code),
    'h_c': False,
    'usr_country': country_code,
    'country_list': country_list,
    'msg_data_eb': msg_data_eb,
    'eb': eb,
    'msg_data_sent': msg_data_sent,
    'msg_data_rec': msg_data_rec,
    'title': 'Committee'
})
    

@app.post('/send_message')
async def send_message(data: sendMessages):
    email = data.email
    host_code = data.host_code
    user = session.query(User).filter_by(person=email, host_code=host_code).first()
    if user:
        message = data.message
        from_c = user.post
        message_adder_dab(message['host_code'],message['to_c'],from_c,message['viaeb'],message['message'],message['replyid'],message['chit_pnt'])
    pass



@app.post('/email_sign_up')
async def email_add(data: emailAdd):
    try:
        email = data.email
        if "@" not in email or session.query(Person).filter_by(email=email).first() is not None:
            return {"status":"Failed"}
        #request.session["person"] = email 
        add_email(email)
        return {"status":"Success"}
    except:
        return {"status":"Failed"}


@app.post('/mun_page')
async def mun_page(data: munPage):
    person1 = session.query(Person).filter_by(email=data.email).first()#harshdipashah@gmail.com
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


@app.post('/mun_reg')
async def mun_reg(data: munReg):
    email=data.email
    host_code = data.host_code
    if session.query(User).filter_by(person=email, host_code=host_code).first() is not None:
        return {"status":"Failed"}
    else:
        try:
            user = User(
            person=email,
            host_code=host_code,
            post='',
            auto_reply_switch=False,
            attendance=True
            )
            session.add(user)
            session.commit()
            return {"status":"Success"}
        except:
            return {"status":"Failed"}
        
    
    
    
