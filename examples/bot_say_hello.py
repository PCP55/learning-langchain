# This example is just a example of how to get message and response to Slack.

import os

from dotenv import load_dotenv
from flask import Flask
import slack
from slackeventsapi import SlackEventAdapter

load_dotenv()

ENV_NAME = os.getenv("ENV_NAME")
SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")

if ENV_NAME is None:    
    raise "Cannot load .env file properly"


app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, '/slack/events', app)

client = slack.WebClient(token=SLACK_TOKEN)
client.chat_postMessage(channel="#learning-langchain", text="Hello human")


@ slack_event_adapter.on('message')
def message(payload):
    print(payload)
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    if text == "hi":
        client.chat_postMessage(channel=channel_id,text="Hello")


if __name__ == "__main__":
    app.run(debug=True)
