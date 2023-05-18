import os

from dotenv import load_dotenv
from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.llms import OpenAI, HuggingFaceHub
from langchain.prompts import PromptTemplate
import pandas as pd
import sqlite3

load_dotenv()

ENV_NAME = os.getenv("ENV_NAME")
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
HUGGINGFACE_HUB_API_KEY = os.getenv("HUGGINGFACE_HUB_API_KEY")

if ENV_NAME is None:
    raise "Cannot load .env file properly"


DATABASE_PATH = "examples/bot_with_langchain/data/titanic.db"

PROMPT_TEMPLATE = """
You have access to the following SQL tables that describe the passengers of the Titanic:
Table 1: survivors with columns: PassengerId and Survived. The survived column indicates whether a person has survived the Titanic disaster. 0 if not, 1 if yes.
Table 2: tickets with columns: PassengerId, Ticket - ticket id, Pclass - passenger class (1, 2, or 3), Fare - passenger fare, Cabin - cabin number, Embarked - the port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)
Table 3: passengers with columns: PassengerId, Name, Sex (words "male" or "female"), Age, SibSp - the number of siblings/spouses aboard the Titanic, Parch - the number of parents/children aboard the Titanic

When you are asked to retrieve data, return a SQL query using the provided tables.
###
{query}
"""


class AI:
    def __init__(self, sql_query):
        # self.llm = HuggingFaceHub(repo_id="google/flan-t5-xl", huggingfacehub_api_token=HUGGINGFACE_HUB_API_KEY, model_kwargs={"temperature":0, "max_length":64})
        # self.llm = HuggingFaceHub(repo_id="pythainlp/wangchanglm-7.5B-sft-enth-sharded", huggingfacehub_api_token=HUGGINGFACE_HUB_API_KEY)
        # self.llm = HuggingFaceHub(repo_id="gpt2", huggingfacehub_api_token=HUGGINGFACE_HUB_API_KEY)
        self.llm = OpenAI(model_name="text-davinci-003", temperature=0.5, openai_api_key=OPEN_AI_API_KEY)
        # self.llm = OpenAI(model_name="ada", temperature=0.9, openai_api_key=OPEN_AI_API_KEY)
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
            max_iterations=5,
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
