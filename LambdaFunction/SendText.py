import os
from twilio.rest import Client

# numbers must be in E.164 format
def send_text(acc_sid, auth_token, from_num, text_filename, to_num):
    client = Client(acc_sid, auth_token)
    with open('/tmp/' + text_filename, 'r') as myfile:
        body_text = myfile.read()
        message = client.messages.create(
                                  from_=from_num,
                                  body=body_text,
                                  to=to_num
                              )
