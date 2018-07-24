#!/usr/bin/env python3
# Python Version 3.7.0
import requests

def subscribe(user_id, callback, client_id, duration, secret=None):
    payload = {'hub.mode' : 'subscribe', 'hub.topic' : 'https://api.twitch.tv/helix/streams?user_id=' + user_id,
                'hub.callback' : callback, 'hub.lease_seconds' : duration, 'hub.secret' : secret}
    head = {'Client-ID' : client_id, 'Content-Type' : 'application/json'}
    resp = requests.post('https://api.twitch.tv/helix/webhooks/hub', json=payload, headers=head)
    print(resp.status_code)

# This is used to invoke the streaming part of a larger program on AWS Lambda
subscribe(--enter your parameters here--)
