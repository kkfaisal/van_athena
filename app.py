from vanna.pgvector import PG_VectorStore
from vanna.openai import OpenAI_Chat
from vanna.remote import VannaDefault
from openai import OpenAI
import os
from vanna.flask import VannaFlaskApp
from auth_ui import SimplePassword
from athena_utils import run_athena_query,validate_athena_query
import pandas as pd

openai_api_key = os.environ['OPENAI_API_KEY']
vector_connection_string = "postgresql://vector_user:vector_pass@postgres-vector:5432/vector_db"

deepseek_client = OpenAI(api_key=openai_api_key, base_url="https://api.deepseek.com")

class CustomVanna(PG_VectorStore, OpenAI_Chat):

    def __init__(self, config=None):
        PG_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self,client=deepseek_client, config=config)
    
        self.dialect = "AWS Athena(Trino)"

    # This is to control whn to generate a chart. Change it as your need. also omiit this to use dfault function.
    def should_generate_chart(self, df: pd.DataFrame) -> bool:
         return True
    
    def generate_sql(self, question,allow_llm_to_see_data=True, **kwargs) -> str:
        # Add Athena-specific prefix to the prompt
        athena_prefix = """You are querying an Amazon Athena database. 
        Please generate SQL that is compatible with Athena's SQL syntax.
        Original question: """
        
        modified_prompt = f"{athena_prefix} {question}"
        
        # Must return the result
        return super().generate_sql(modified_prompt, allow_llm_to_see_data=allow_llm_to_see_data, **kwargs)

vn = CustomVanna(config={'model': 'deepseek-chat', "connection_string": vector_connection_string})
vn.run_sql = run_athena_query
vn.run_sql_is_set = True
vn.validate_sql = validate_athena_query

app = VannaFlaskApp(
    vn=vn,
    #Change your password and add more users as needed. This is should kept as seceret file in aws secret manger and load as needed
    auth=SimplePassword(users=[{"email": "admin@example.com", "password": "*********"}]),
    allow_llm_to_see_data=True,
    title="CAFU Data Lake Query",
    subtitle="Talk to Data Lake in English",
    show_training_data=True,
    logo="https://pic.surf/e93",
    sql=True,
    table=True,
    chart=True,
    summarization=False,
    ask_results_correct=True,
).run()
