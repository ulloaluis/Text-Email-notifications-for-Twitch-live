# Text/Email Notifications for Twitch.tv
## What's in store
New Twitch API - Webhooks in Python 3.6, AWS Lambda, CloudWatch logging, AWS SES, Twilio API, Python requests library, callback handlers, and lots of json fun

## General overview of how this program does what it does
I send a POST request to the New Twitch API Webhooks feature, in which I include a callback url. This callback url is a link to an API Gateway that serves as a proxy for my AWS Lambda function. My lambda function is set up as a callback handler that will deal with the two main cases: 

1) We are responding to the challenge from the twitch api by returning their challenge string---this proves to them that this is our valid callback url.

2) We are already subscribed to updates through the webhook since we've done step 1, and the streamer has just gone live! In this case, we parse the body of their response and use the data to create the message we want to send to our email/phone. This message is written to a file called message.txt. The send_email and send_text functions get their parameters (which is sensitive information, like api keys) from a json file, and the message they send is from message.txt.

  a) send_email - using AWS SES, the preferred way to send emails through AWS (no, seriously, they make it very difficult to use anything else).
  
  b) send_text - using Twilio API. This was very straightforward to implement; they have a wonderful API. I will include a link later in this read me that allows you to do it in a couple of lines.
  
Comments: A lot of the tools I used in this program were very new to me, so there might be better ways of implementing certain parts of the code. If you notice anything that can be improved, please let me know! Useful/relevant links will be at the end of this readme.


## Getting set-up
One file can be run from your local computer, but the rest will be on AWS Lambda. The one file is the code for the initial POST request you send to Twitch, which then starts the interactions between your AWS Lambda code and the Twitch API Webhook. Note that you will need to install the requests library to run that code. (pip3 install requests)

1) Download the code in the "Lambda function code" folder.

2) Fill out the data.json folder --see data.json subsection (includes getting API keys)

3) Install its dependencies into the same folder 

  3a) This includes Twilio (for texts) and boto3 (for emails). You can use the following command while in the folder:
  
    format --> pip install module-name -t /path/to/project-dir
  
    If you are using python 3,
    
    pip3 install twilio -t /path/to/project-dir
  
    pip3 install boto3 -t /path/to/project-dir

4) zip the contents of this folder (without zipping the folder)

    4a) Go into the AWS Lambda folder and run this command: 
    
            zip -r alerts.zip ./*
          
      This will zip the contents of the folder into alerts.zip.

5) Create a new AWS Lambda function and an API Gateway
    5a) If you don't care too much about security right now and just want to get a working version, make your rules as permissive as possible.
    5b) Once again, it's possible to make your API Gateway as permissive as possible. If you decide to add rules, make sure you can accept GET and POST notifications, since Twitch API will utilize both of those. The callback url would be the invoke url on the API Gateway. (The API Gateway is added as a trigger under the lambda function.)

6) Upload the code as a zip file, you will probably get "file too large, but can still call function" notification, which is fine. However, if you have to change your code, you will have to re-zip and re-upload the file (there's probably a much better way to do this, but I've been doing it that way).

7) [Verify an email address](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses-procedure.html) that you can then use with Amazon SES.

8) Call the local computer script, TwitchAPIStreaming.py, with the appropriate parameters. --see TwitchAPIStreaming.py section

9) After calling the local computer script, you can check inside CloudWatch logs to see if it was successful. Or, you could have the streamer go online and see if you get a text or email! (Or do what I did and pass in your own user_id, download OBS for Twitch streaming, so you could test it without someone else's help)

## data.json setup
### For the twilio portion
Account SID and authorization token can be found on the Twilio website after you set up an account

"to_num" is the number that the message is sent to. Should be in E.164 format:

> Format this number with a '+' and a country code, e.g., +16175551212

"from_num" should have the same format as to_num. This is your twilio phone number. You can get one for free under the getting started location in the phone number dashboard (# symbol).

"text_filename" can remain as message.txt. This is the file with the message being sent. It is written to at some point, so it is fine if that file is empty initially.

### For the email portion

[Use the boto3 docs, under the send_email function](https://boto3.readthedocs.io/en/latest/reference/services/ses.html#SES.Client.send_email). Note that if you decide to add more parameters than those given, you CANNOT include an empty parameter, like an empty list. The documentation does this and it is wrong and misleading; your code will not work. (It is fine for that part to be empty in the json file, just don't include it as a parameter)

## TwitchAPIStreaming.py setup
You will have to supply a user_id, callback url, client_id, duration time, and secret (secret will default to None).

### user_id
This is the user_id of the person you are subscribing to for stream-is-live updates. I think the best way to get the user_id is to use [this chrome browser extension](https://chrome.google.com/webstore/detail/twitch-username-and-user/laonpoebfalkjijglbjbnkfndibbcoon), in which you just put in a twitch username and it returns the user_id, or vice versa.

### callback url
This is the invoke url of the API Gateway listed as a trigger under the AWS Lambda function. It is mentioned earlier under step #5.

### client_id
This is your client_id. In order to get this, you have to head over to the twitch developer page, create an account, and start an app. Under that app, your client_id will be listed. There's a redirect url on there as well that defaults to localhost, and although I haven't tested it explicitly just yet, I believe changing that to your callback_url will be useful (if not necessary) for adding more features.

### duration time 
Subscriptions are not indefinite. The max time is 864000, which is 10 days. After that, you will have to run the TwitchAPIStreaming.py script again with the same parameters in order to reset your subscription. (by subscriptions, I meant to the webhook, which is sending a notification payload to your lambda function whenever the streamer goes live)

### secret
This is used as verification. I haven't done anything with this yet, bit will be implementing it later on. It's highly recommended that you use secrets; it's used to verify that you're not getting sent bogus data from a random source!

## Things to do
Add proper sha256 secrets and better API Gateway rules.

Any additional required error checking should be added.

~~Get username from user_id and include in message.txt.~~
![username: crimsonmhp](https://raw.githubusercontent.com/ulloaluis/Text-Email-notifications-for-Twitch-live/master/samples/Screen%20Shot%202018-07-26%20at%202.25.33%20PM.png)

*Could change time displayed to be in user-specified time-zone, if made into an app, will add that functionality.

Set up my program in an app of some sort that allows users to subscribe for text and/or email updates without having to go through the entire process described above!

## Useful Links
[Twitch Webhooks documentation 1](https://dev.twitch.tv/docs/api/webhooks-guide/)

[Twitch Webhooks documentation 2](https://dev.twitch.tv/docs/api/webhooks-reference/#)

[Twitch dev forums (hit or miss)](https://discuss.dev.twitch.tv/)

[Creating a "deployment package"](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html), a.k.a. the zipped folder

[AWS Lambda functions in Python](https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model.html)


## Random Notes

[Postman](https://www.getpostman.com/) is a good way to test your API Gateway with GET/POST to see if everything is behaving as expected. Take care in matching Twitch API's response exactly, easy to mess it up.

query string parameters: link?param1=value&param2=value...

The event object in AWS Lambda will contain the data you want to parse, the context object doesn't really communicate too much with the outside world and only reports on the state of the program, so don't worry too much about the context variable.

Using print statements will log that data to CloudWatch under the lambda function.

Sometimes, things coming through the API Gateway won't get logged. I recommend setting up a [CloudWatch for the Gateway specifically](https://kennbrodhagen.net/2016/07/23/how-to-enable-logging-for-api-gateway/). This was a small quirk I found during this project, and I may be wrong about it, but setting up this gateway logger allowed me to view more logged data than that within the normal lambda logging nonetheless.

I don't recommend curl-ing your API Gateway (can get unruly with all the parameters you need), although it is one way to check if your server is working properly. I think it's pointless to do this if you can just run the normal script and then check the logs.

The twitch webhooks api initial subscription is looking for the hub.challenge string and nothing else. Place this string into the "body" of your response. 

There are a lot more examples of slack api webhook callback handlers in python than there are examples of twitch api webhook callback handlers in python, and I'm glad I could change this.

