from agents.agent import AI, sql_query

import os
from threading import Thread
from queue import Queue, Full

from dotenv import load_dotenv
from flask import Flask
import slack
from slackeventsapi import SlackEventAdapter

from utils.slack_utils import reply_to_slack, confirm_message_received

load_dotenv()

ENV_NAME = os.getenv("ENV_NAME")
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")

if ENV_NAME is None:
    raise "Cannot load .env file properly"


def handle_message():
    while True:
        message_id, thread_ts, user_id, text = messages_to_handle.get()
        print(f'Handling message {message_id} with text {text}')
        text = " ".join(text.split(" ", 1)[1:])
        try:
            response = ai.run(text)
            # response = "I'm sleeping. Please don't disturb."
            reply_to_slack(client, thread_ts, response)
        except Exception as e:
            response = f":exclamation::exclamation::exclamation: Error: {e}"
            reply_to_slack(client, thread_ts, response)
        finally:
            messages_to_handle.task_done()


app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, '/slack/events', app)


@ slack_event_adapter.on('app_mention')
def message(payload):
    print(payload)
    event = payload.get('event', {})

    message_id = event.get('client_msg_id')
    thread_ts = event.get('ts')
    channel = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    try:
        messages_to_handle.put_nowait((message_id, thread_ts, user_id, text))
        confirm_message_received(client, channel, thread_ts)
    except Full:
        response = ":exclamation::exclamation::exclamation:Error: Too many requests"
        reply_to_slack(client, thread_ts, response)
    except Exception as e:
        response = f":exclamation::exclamation::exclamation: Error: {e}"
        reply_to_slack(client, thread_ts, response)
        print(e)


if __name__ == "__main__":
    ai = AI(sql_query)
    messages_to_handle = Queue(maxsize=32)
    client = slack.WebClient(token=SLACK_TOKEN)

    Thread(target=handle_message, daemon=True).start()
    app.run(debug=True)
