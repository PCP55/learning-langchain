from agents.agent import AI, sql_query

import os

from dotenv import load_dotenv


load_dotenv()


ENV_NAME = os.getenv("ENV_NAME")
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")

if ENV_NAME is None:
    raise "Cannot load .env file properly"


if __name__ == "__main__":
    text = input("What do you want me to do?\n")
    text = " ".join(text.split())

    ai = AI(sql_query)

    try:
        response = ai.run(text)
        # response = "I'm sleeping. Please don't disturb."
    except Exception as e:
        response = e
    finally:
        print(f"Response: {response}")
