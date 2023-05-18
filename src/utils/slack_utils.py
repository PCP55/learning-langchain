slack_channel = "#learning-langchain"


def reply_to_slack(client, thread_ts, response):
    client.chat_postMessage(channel=slack_channel, text=response, thread_ts=thread_ts)


def confirm_message_received(client, channel, thread_ts):
    client.reactions_add(
        channel=channel,
        # name="thumbsup",
        name="thinking_face",
        timestamp=thread_ts
    )