from openai import OpenAI
import os
from prompts import basic
import SQLFuntime
from dotenv import load_dotenv, find_dotenv

print("DOTENV FILE:", find_dotenv())  # which .env is it using?
load_dotenv()

print("OPENAI_API_KEY:", repr(os.getenv("OPENAI_API_KEY")))

# Reads OPENAI_API_KEY from your environment)
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
print(os.environ["OPENAI_API_KEY"])
            #user_text: str, 
prompt = SQLFuntime.get_admin("Davidfriedchicken@gmail.com", "TheEverLateStudent")
print("From de aiResponse line 17: " + prompt[0][3])
def ai_reply(num) -> str:
    messagesArr = SQLFuntime.get_messages(num)
    messages = ""

    for message in messagesArr:
        messages = messages + message + "\n\n"

    print(f"{prompt[0][3]}  {messages}")

   # print("From aiResponse.py \n\n\n " + f"{basic.basicPromt}  {messages}")
    resp = client.responses.create(
        model="gpt-5",               # pick your model
        input=f"{prompt[0][3]}  {messages}"
    )
    print(resp)
    SQLFuntime.insert_message(num, "Sarah: " + resp.output_text.strip())
    return resp.output_text.strip()

#  if __name__ == "__main__":
#      print(ai_reply("Hey, are you open on weekends?"))