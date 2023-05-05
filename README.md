# learning-langchain

This repository is about interacting with `langchain` LLM via Slack.

# Setup Slack

An simple example is `bot.py` file.

There are several steps to implement.

1. Setup Slack: 
   
   https://www.pragnakalp.com/create-slack-bot-using-python-tutorial-with-examples/

2. Setup `ngrok` and expose localhost to Slack

        ngrok http http://127.0.0.1:5000

3. Go to Slack Event Subscriptions at `https://api.slack.com/apps/<your_app_id_from_url>/event-subscriptions?` and add public dns from `ngrok`


# Integrate Langchain

1. After setup Slack, you can follow a below instruction for your first bot. An simple example is `bot_with_langchain.py` file.

    https://www.mikulskibartosz.name/ai-data-analyst-bot-for-slack-with-gpt-and-langchain/

2. Feel free to custom your bot as I did in `/src/` folder.


# Monitor the system
Lastly, implementing Langchain on Production can be difficult to monitor and evaluate. Here is one of the example explaining how to monitor and evaluate Langchain:

https://www.youtube.com/watch?v=bfwvqjgfAZw&list=WL&index=33&t=34s&ab_channel=KamalrajMM

---

# References

Want to learn more about Langchain? Please go to:
- https://www.youtube.com/watch?v=aywZrzNaKjs&list=WL&index=31&ab_channel=Rabbitmetrics
- https://www.youtube.com/watch?v=LbT1yp6quS8&ab_channel=PatrickLoeber
- https://www.youtube.com/watch?v=MlK6SIjcjE8&list=WL&index=30&t=16s&ab_channel=NicholasRenotte

OpenAI
- https://platform.openai.com/docs/api-reference

Hugging Face
- https://huggingface.co/