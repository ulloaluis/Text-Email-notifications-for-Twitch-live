from SendEmail import send_email
from SendText import send_text
import json
import os

def response(message, code):
    return {
        'statusCode': code,
        'headers': {'Content-Type': 'application/json'},
        'body': message
    }

# Callback handler that receives either 1) a challenge for verifying
# a webhook subsciption or 2) a notification payload with details about
# a streamer going on/off-line, in which case we write to message.txt and
# then send a text and email
# *print function is used for cloud watch logging*
def lambda_handler(event, context):
    print(event)
    if event.get('queryStringParameters') and event['queryStringParameters'].get('hub.challenge'): # must not be None
        print(event['queryStringParameters']['hub.challenge'])
        message = event['queryStringParameters']['hub.challenge']
        return response(message, 200)
    elif 'body' in event and event['body']: # body exists and is not None
        body = json.loads(event['body']) # currently a string, load as json
        if len(body.get('data')) > 0: # data is well-formed (would be size 1 with {data here})
            with open('/tmp/message.txt', 'w') as msg: # update message file
                start_time = body['data'][0]['started_at']
                stream_title = body['data'][0]['title']
                msg.write("Now streaming since %s: %s" % (start_time, stream_title))
            with open('/'.join([os.path.dirname(__file__), 'data.json']), 'r') as f: # send email/text
                data = json.load(f) # json file must be in same directory!
                send_email(data['Email'])
                send_text(*data['Twilio-SMS'].values())
            message = 'Successful email and text send!'
            return response(message, 200)
        else: # data is an empty array, stream offline
            message = 'Stream Offline.'
            return response(message, 200)
    else:
        message = 'Something went wrong/is malformed.'
        return response(message, 500)
