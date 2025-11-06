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
async def inbound_message(payload: TextbeltReply):
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
    print("From inbound. text is this: " + payload.text + "\n\n" + payload.fromNumber + "\n\n\n")
    res = SQLFuntime.insert_message(payload.fromNumber, "customer:" + payload.text)
    if res == False:
        print("No number found.")
        return ValueError
    Response = ai_reply(payload.fromNumber)
    sendSMS(payload.fromNumber, Response)
    

    print("From inbound. messages is this: " + str(SQLFuntime.get_messages(payload.fromNumber)) + "\n\n")

    print(f"[Textbelt reply] textId={payload.textId} from={payload.fromNumber} text={payload.text}")
    return {"ok": True}

    #messages = sendSMS(payload["from"], payload["text"])
    #print(payload)
    #print(messages)
    #return messages





@app.get("/test")
async def inbound_message(request: Request):
    return SQLFuntime.find_numbers()
    