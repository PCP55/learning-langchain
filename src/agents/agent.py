import os

from dotenv import load_dotenv
from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import pandas as pd
import sqlite3

from utils.agent_utils import get_prompt_agent_config

load_dotenv()

ENV_NAME = os.getenv("ENV_NAME")
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
HUGGINGFACE_HUB_API_KEY = os.getenv("HUGGINGFACE_HUB_API_KEY")

if ENV_NAME is None:
    raise "Cannot load .env file properly"


DATABASE_PATH, PROMPT_TEMPLATE = get_prompt_agent_config(topic_name = "introduction")


class AI:
    def __init__(self, sql_query):
        self.llm = OpenAI(model_name="text-davinci-003", temperature=0.5, openai_api_key=OPEN_AI_API_KEY)
        self.prompt = PromptTemplate(
            input_variables=["query"],
            template=PROMPT_TEMPLATE,
        )
        self.tools = [
            Tool(
                name="SQL",
                func=sql_query,
                description="Runs a given SQL query and returns response as Markdown",
            )
        ]
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent="zero-shot-react-description",
            verbose=True,
            max_iterations=2,
        )

    def run(self, query):
        print("ai start run")
        print(f"query: {query}")
        agent_prompt = self.prompt.format(query=query)
        return self.agent.run(agent_prompt)


def run_query(query):
    con = sqlite3.connect(DATABASE_PATH)
    try:
        print(f"SQL query: {query}")
        response = pd.read_sql_query(query, con)
        print(f"SQL Response: {response}")
        return response
    finally:
        con.close()


def sql_query(query):
    return run_query(query).to_markdown()
