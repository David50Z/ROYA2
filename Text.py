# import smtplib
# from email.message import EmailMessage

# def text(subject, body, to):
#     msg = EmailMessage()
#     msg.set_content(body)
#     msg['subject'] = subject
#     msg['to'] = to
    
#     user = "trentonblackthorn@gmail.com"
#     msg['from'] = user
#     password = "Dawkinator73"

#     server = smtplib.SMTP("smtp.gmail.com", 587)
#     server.starttls()
#     server.login(user, "qeyu imlk cidf sjmd")
#     server.send_message(msg)

#     server.quit()


# if __name__ == '__main__':
#     text("Hey", "Hello world", "7256001255@sms.myboostmobile.com")

#     print("Yo")



# from twilio.rest import Client
# import keys

# print(keys.account_sid)
# print(keys.auth_token)

# client = Client(keys.account_sid, keys.auth_token)

# message = client.messages.create(
#     body = "This is a new message from Code Palace!",
#     from_=keys.twilio_number,
#     to=keys.my_phone_number
# )


# print(message.body)



# import vonage
# import keys

# client = vonage.Client(key=keys.vonage_key, secret=keys.vonage_secret)
# sms = vonage.Sms(client)


# responseData = sms.send_message(
#     {
#         "from": "12394435296",
#         "to": "17256001255",
#         "text": "A text message sent using the Nexmo SMS API",
#     }
# )

# if responseData["messages"][0]["status"] == "0":
#     print("Message sent successfully.")
# else:
#     print(f"Message failed with error: {responseData['messages'][0]['error-text']}")



import os
from vonage import Vonage, Auth
from vonage_sms import SmsMessage
import SQLFuntime
import requests
text_key=os.environ["TEXT_KEY"]
textbee_key = os.environ["TEXTBEE_KEY"]
bearer = os.environ["BEARER"]
url = os.environ["URL"]
message = "Sarah: It’s Sarah from Meridian Health. Is this the same Kevin that got a quote from us in the last couple of months?"
def sendInitialSMS(num: str):

    # headers = {
    #     "message": "Yo",
    #     "recipients": [
    #         "7256001255"
    #     ]
    # }

    headers = {
        "x-api-key": textbee_key,
         "Authorization": f"Bearer {bearer}",
        "Content-Type": "application/json",
        "Accept": "*/*",
    }

    payload ={
            "message": "It’s Sarah from Meridian Health. Is this the same Kevin that got a quote from us in the last couple of months?",
            "recipients": [
            num
        ]
    
    }

    # headers = {
    # 'x-api-key': API_KEY,
    # },

    #print(text_key)
    # resp = requests.post('https://textbelt.com/text', {
    # 'phone': str(num),
    # 'message': "It’s Sarah from Meridian Health. Is this the same Kevin that got a quote from us in the last couple of months?",
    # 'key': text_key,
    # 'replyWebhookUrl': url + '/inbound',
    
    # })


    # resp = requests.post('https://api.textbee.dev/api/v1/gateway/devices/691adbde82033f160912e113/sendSMS', {
    #         "message": "Yo",
    #         "recipients": [
    #         "7256001255"
    #     ]
    
    # }, {
    #     "headers": {
    #     'x-api-key': textbee_key,
    # }
    # })


    resp = requests.post('https://api.textbee.dev/api/v1/gateway/devices/691adbde82033f160912e113/sendSMS', 
                         json=payload,
                         headers=headers
                         )


    SQLFuntime.create_number(num, message)
    return resp.text

def sendSMS(num: str, text: str):
    # resp = requests.post('https://textbelt.com/text', {
    # 'phone': str(num),
    # 'message': text,
    # 'key': text_key,
    # 'replyWebhookUrl': url + '/inbound',

    
    # })

    headers = {
        "x-api-key": textbee_key,
         "Authorization": f"Bearer {bearer}",
        "Content-Type": "application/json",
        "Accept": "*/*",
    }

    payload ={
            "message": text,
            "recipients": [
            "7256001255"
        ]
    
    }

    resp = requests.post('https://api.textbee.dev/api/v1/gateway/devices/691adbde82033f160912e113/sendSMS', 
                    json=payload,
                    headers=headers
                    )
    return resp.text
    

if __name__ == "__main__":
    #sendSMS("+17256001255", "Hello from Vonage + Python")
    

                            #7028247180
    resp = sendInitialSMS(str(17024478136))
    
    print(resp)