from vanna.pgvector import PG_VectorStore
from vanna.openai import OpenAI_Chat
from vanna.remote import VannaDefault
from openai import OpenAI
import os
from vanna.flask import VannaFlaskApp
from smpl_auth import SimplePassword
from athena_utils import run_athena_query,validate_athena_query

openai_api_key = os.environ['OPENAI_API_KEY']
# connection_string = "postgresql://pgv_user:pgv_pass@localhost:5432/pgv"

#for docker
connection_string = "postgresql://vector_user:vector_pass@postgres-vector:5432/vector_db"

deepseek_client = OpenAI(api_key=openai_api_key, base_url="https://api.deepseek.com")

class CustomVanna(PG_VectorStore, OpenAI_Chat):

    def __init__(self, config=None):
        PG_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self,client=deepseek_client, config=config)
        self.dialect = "AWS Athena(Trino)"
    def generate_sql(self, question,allow_llm_to_see_data=True, **kwargs) -> str:
        # Add Athena-specific prefix to the prompt
        athena_prefix = """You are querying an Amazon Athena database. 
        Please generate SQL that is compatible with Athena's SQL syntax.
        Original question: """
        
        modified_prompt = f"{athena_prefix} {question}"
        
        # Must return the result
        return super().generate_sql(modified_prompt, allow_llm_to_see_data=allow_llm_to_see_data, **kwargs)

vn = CustomVanna(config={'model': 'deepseek-chat', "connection_string": connection_string})
vn.run_sql = run_athena_query
vn.validate_sql = validate_athena_query

print("=================")
# The information schema query may need some tweaking depending on your database. This is a good starting point.
inf_schema_query = """
SELECT 
'AwsDataCatalog' as database, table_schema, table_name, column_name, data_type 
FROM 
information_schema.columns 
WHERE table_schema = '<athena_dbs>' AND 
table_name = '<athena_table>' 
ORDER BY ordinal_position ASC;
    """
df_information_schema = vn.run_sql(inf_schema_query)
print(f"df_information_schema: {df_information_schema}")
# This will break up the information schema into bite-sized chunks that can be referenced by the LLM
plan = vn.get_training_plan_generic(df_information_schema)

print(f"Plan: {plan}")
vn.train(plan=plan)

# # train on docs
 #read line of /train_doc_1.txt
with open('/Users/faisalfalah/Desktop/CAFU/code/cafu-de-redshift-utils/vanna.ai/train_doc_1.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        vn.train(documentation=line)
