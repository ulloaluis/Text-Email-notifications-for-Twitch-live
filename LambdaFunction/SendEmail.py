import os
import boto3
import json # since data is json
def send_email(data): # received json dict data for email
    # AWS temp folder system
    with open('/tmp/message.txt', 'r') as myfile:
        body_text = myfile.read()
    # using Python AWS SDK for AWS SES since AWS refuses to accept SMTP library
    client = boto3.client('ses', region_name='us-east-1') # region will vary!
    response = client.send_email(
        Source=data['Source'],
        Destination=data['Destination'],
        Message={"Body": { "Text": { "Data": body_text, "Charset": "UTF-8"}},
                 "Subject": {"Data": "Twitch Alert!", "Charset": "UTF-8"}}
        # ReplyToAddresses=data['ReplyToAddresses'],
        # ReturnPath=data['ReturnPath'],
        # SourceArn=data['SourceArn'],
        # ReturnPathArn=data['ReturnPathArn']
        # Tags=data['Tags'],
        # ConfigurationSetName=data['ConfigurationSetName']
    )
    print(response) # log data
