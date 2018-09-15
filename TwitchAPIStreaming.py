#!/usr/bin/env python3
import requests
from PrivateConstants import API_GATEWAY, CLIENT_ID, SECRET

MAX_DURATION = '864000'  # 10 days is maximum subscription, can renew repeatedly


def name_to_id(name):
    """Convert name to id by asking the twitch api. Precondition: user exists."""
    head = {'Client-ID': CLIENT_ID, 'Content-Type': 'application/json'}
    resp = requests.get('https://api.twitch.tv/helix/users?login=' + name, headers=head)
    json_data = resp.json()
    return json_data['data'][0]['id']


def user_exists(user):
    """Attempt to get user from twitch api."""
    head = {'Client-ID': CLIENT_ID, 'Content-Type': 'application/json'}
    resp = requests.get('https://api.twitch.tv/helix/users?login=' + user, headers=head)
    json_data = resp.json()
    return len(json_data['data']) > 0  # not an empty array


def days_to_seconds(days):
    """86,400 seconds in a day."""
    return int(days*86400)


def subscribe(user, time):
    """ Invokes AWS Lambda which then requests the subscription to
    :param user: user being subscribed to, in id form (str)
    :param time: duration of subscription in seconds (int)
    :return: status code of response, for verifying if successful
    """
    payload = {'hub.mode': 'subscribe', 'hub.topic': 'https://api.twitch.tv/helix/streams?user_id=' + user,
               'hub.callback': API_GATEWAY, 'hub.lease_seconds': time, 'hub.secret': SECRET}
    head = {'Client-ID': CLIENT_ID, 'Content-Type': 'application/json'}
    resp = requests.post('https://api.twitch.tv/helix/webhooks/hub', json=payload, headers=head)
    return str(resp.status_code)


if __name__ == "__main__":
    user, days = None, MAX_DURATION
    print("Welcome to the text and email Twitch subscription program.")
    while True:
        user = input("Please input the name of the user you would like to subscribe to: ")
        while not user_exists(user):
            user = input("Please enter a valid username: ")

        days = float(input("Please enter, in days, how long you would like to be subscribed for (Max=10.0): "))
        while days > 10.0 or days < 0.0:
            days = float(input("Please enter a valid number of days (0.0-10.0): "))

        status_code = subscribe(name_to_id(user), days_to_seconds(days))
        if status_code.startswith('2'):  # success = status codes 2xx
            print("You were successfully subscribed to {0} for {1} days.".format(user, days))

        more = input("Would you like to do another subscription (yes/no)? ")
        if more == "no":
            print("Goodbye.")
            break
