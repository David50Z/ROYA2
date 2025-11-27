from fastapi import FastAPI, Body, HTTPException, Form, UploadFile, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
#from passlib.context import CryptContext
import os
import sys
import psycopg2
from pydantic import BaseModel
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
import SQLFuntime
from Text import sendInitialSMS, sendSMS
from aiResponse import ai_reply

class TextbeltReply(BaseModel):
    textId: str | None = None
    fromNumber: str | None = None
    text: str | None = None


app = FastAPI()

origins = [
    "http://localhost:5173",   # Svelte dev
    "https://your-frontend.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # use ["*"] only if NOT using cookies/Authorization
    allow_credentials=False,         # if you send cookies or Authorization
    allow_methods=["*"],
    allow_headers=["*"],            # or list specific: ["Content-Type","Authorization"]
)

@app.get("/")
async def inbound_message(request: Request):

    return {"Hello":"world"}


@app.post("/inbound")
async def inbound_message(request: Request):
    data = await request.json()
    # q = request.query_params  # starlette.datastructures.QueryParams
    # payload = {
    #     "from": q.get("msisdn"),
    #     "to": q.get("to"),
    #     "text": q.get("text"),
    #     "message_id": q.get("messageId"),
    #     "timestamp": q.get("message-timestamp"),
    #     "keyword": q.get("keyword"),
    #     "type": q.get("type"),
    #     "api_key": q.get("api-key"),
    # }
    if data["sender"] != "+17024478136" or data["sender"] != "+17028247180" or data["sender"] != "+17256001255":

        print("From inbound. text is this: " + data["message"] + "\n\n" + data["sender"] + "\n\n\n")
        res = SQLFuntime.insert_message(data["sender"], "customer:" + data["message"])
        if res == False:
            print("No number found.")
            return ValueError
        Response = ai_reply(data["sender"])
        sendSMS(data["sender"], Response)
        

        print("From inbound. messages is this: " + str(SQLFuntime.get_messages(data["sender"])) + "\n\n")

        print(f"[Textbelt reply] textId={data['smsId']} from={data['sender']} text={data['message']}")
        return {"ok": True}
    
    else:
        print("Invalid sender")
        return {"ok": "Invalid sender"}

    #messages = sendSMS(payload["from"], payload["text"])
    #print(payload)
    #print(messages)
    #return messages





@app.post("/test")
async def inbound_message(request: Request):
    data = await request.json()
    print("JSON BODY:", data)
    return SQLFuntime.find_numbers()


@app.get("/text")
async def outbound_message(request: Request, num: int):
    res = sendInitialSMS(num)
    return {"return": str(res)}
    

@app.get("/test-ai")
async def outbound_message(request: Request):
    res = ai_reply("+7256001255")
    return {"return": str(res)}
    

@app.post("/create-account")
async def create_account(
    email: str = Body(...), 
    password: str = Body(...),
    prompt: str = Body(...),
    ):

    res = SQLFuntime.checkEmail(email)

    if res == False:
         print("Twas double false from main.py")
         return False
    else:

        row = SQLFuntime.create_admin(email, password, prompt)
        return row
    
@app.post("/reset-number")
async def resetText(num: int = Body(...)):
    res = SQLFuntime.resetNumber(num)
    return res



@app.post("/login")
async def create_account(
    email: str = Body(...), 
    password: str = Body(...),
    ):
    row = SQLFuntime.get_admin(email, password)
    return row

@app.post("/get-admin-id")
async def create_account(
    id: str = Body(...), 
    ):
    row = SQLFuntime.get_admin_By_Id(int(id))
    return row

@app.get("/check-email")
async def checkEmail(email: str = Body(...),):
     res = SQLFuntime.checkEmail(email)

     if res == False:
         return False
     else:
         return True
     
@app.get("/get-prompt")
async def getPrompt(email: str = Body(...),):
     res = SQLFuntime.getPrompt(email)

     if res == False:
         return False
     else:
         return res
     
@app.post("/update-prompt")
async def getPrompt(email: str = Body(...), prompt: str = Body(...),):
     res = SQLFuntime.updatePrompt(email, prompt)

     if res == False:
         return False
     else:
         return res
     
    