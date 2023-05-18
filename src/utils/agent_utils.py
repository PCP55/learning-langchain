import os
import yaml


def get_prompt_agent_config(topic_name: str):
    with open(os.path.join("./src/topics",topic_name,"prompt_template.yaml")) as reader:
        config_file = yaml.safe_load(reader)
        db_path = config_file["db_path"]
        prompt_template = config_file["prompt"]
        print(f"database path: {db_path}")
    return db_path, prompt_template