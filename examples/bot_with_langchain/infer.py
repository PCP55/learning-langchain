from agents.query_agent import AI, sql_query

import os
from threading import Thread
from queue import Queue, Full

from dotenv import load_dotenv
from flask import Flask
import slack
from slackeventsapi import SlackEventAdapter


load_dotenv()

ENV_NAME = os.getenv("ENV_NAME")
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
SLACK_CHANNEL = "#learning-langchain"
SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")

if ENV_NAME is None:
    raise "Cannot load .env file properly"


def reply_to_slack(thread_ts, response):
    client.chat_postMessage(channel=SLACK_CHANNEL, text=response, thread_ts=thread_ts)


def confirm_message_received(channel, thread_ts):
    client.reactions_add(
        channel=channel,
        name="thumbsup",
        timestamp=thread_ts
    )


def handle_message():
    while True:
        message_id, thread_ts, user_id, text = messages_to_handle.get()
        print(f'Handling message {message_id} with text {text}')
        text = " ".join(text.split(" ", 1)[1:])
        try:
            response = ai.run(text)
            # response = "AI sleeps already"
            reply_to_slack(thread_ts, response)
        except Exception as e:
            response = f":exclamation::exclamation::exclamation: Error: {e}"
            reply_to_slack(thread_ts, response)
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
        confirm_message_received(channel, thread_ts)
    except Full:
        response = ":exclamation::exclamation::exclamation:Error: Too many requests"
        reply_to_slack(thread_ts, response)
    except Exception as e:
        response = f":exclamation::exclamation::exclamation: Error: {e}"
        reply_to_slack(thread_ts, response)
        print(e)


ai = AI(sql_query)
messages_to_handle = Queue(maxsize=32)
client = slack.WebClient(token=SLACK_TOKEN)


if __name__ == "__main__":
    # import sqlite3
    # import pandas as pd
    # DATABASE_PATH = "examples/bot_with_langchain/data/titanic.db"
    # con = sqlite3.connect(DATABASE_PATH)
    # response = pd.read_sql_query("SELECT * FROM survivors LIMIT 1", con)
    # print(response)
    Thread(target=handle_message, daemon=True).start()
    app.run(debug=True)
