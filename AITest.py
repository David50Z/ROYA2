from aiResponse import ai_reply
import SQLFuntime

message = """"It’s Sarah from Meridian Health. Is this the same John that got a quote from us in the last couple of months?"""
SQLFuntime.delete_number("+1777")
SQLFuntime.create_number(777, message)
while True:
    user = input("You: ").strip()
    print(user)
    print("messages before" + str(SQLFuntime.get_messages("+1777")))
    SQLFuntime.insert_message("+1777", user)
    resp = ai_reply("+1777")
    SQLFuntime.insert_message("+1777", resp)
    #print("messages after" + str(SQLFuntime.get_messages("+1777")))
    print(resp)

    if not user:
        continue
    if user.lower() in ("/q", "/quit", "exit"):
        print("Goodbye.")
        break