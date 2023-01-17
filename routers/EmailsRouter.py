#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys


# In[2]:


if sys.path[0][:sys.path[0].rfind("/")] not in sys.path:
    sys.path.append(sys.path[0][:sys.path[0].rfind("/")])


# In[3]:


from Connection import Connection
from fastapi import APIRouter, status, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import mariadb
import smtplib


# In[4]:


router = APIRouter(prefix="/emails",
                            tags=["emails"],
                            responses={404: {"description": "Emails router not found"}})


# In[8]:


from fastapi import FastAPI
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import EmailStr, BaseModel
from typing import List


# In[14]:


conf = ConnectionConfig(
   MAIL_FROM="sensoandsekai@gmail.com",
   MAIL_USERNAME="skjfdnv@yandex.ru",
   MAIL_PASSWORD="tomorrow2014",
   MAIL_PORT=587,
   MAIL_SERVER="smtp.gmail.com",
   MAIL_STARTTLS=True,
   MAIL_SSL_TLS=False
)


# In[17]:


@router.get("/send")
async def send_mail():
 
    template = """
        <html>
        <body>
         
 
<p>Hi !!!
        <br>Thanks for using fastapi mail, keep using it..!!!</p>
 
 
        </body>
        </html>
        """
 
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=["skjfdnv@yandex.ru"],  # List of recipients, as many as you can pass
        body=template,
        subtype="html"
        )
 
    fm = FastMail(conf)
    await fm.send_message(message)
    print(message)
 
     
 
    return JSONResponse(status_code=200, content={"message": "email has been sent"})

