import time
import boto3
import pandas as pd
boto3.setup_default_session(profile_name='cafu-de-admin')
athena_cl = boto3.client('athena', region_name='us-east-1')

def execute_athen_query(query, res_return=True, ath_workgroup='primary'):
    client = athena_cl
    print(f"Running query {query}")

    db = 'cafu_transformed'
    s3_outpt = 's3://cafudataengprod-athena/query_results/users/faisal/'
    print(f"Running query {query}")
    response = client.start_query_execution(
        QueryString=query,
        WorkGroup=ath_workgroup,
        QueryExecutionContext={
            'Database': db
        },
        ResultConfiguration={
            'OutputLocation': s3_outpt,
        },
    )

    query_execution_id = response['QueryExecutionId']

    # get execution status
    while True:
        query_status = client.get_query_execution(QueryExecutionId=query_execution_id)
        query_execution_status = query_status['QueryExecution']['Status']['State']

        if query_execution_status == 'SUCCEEDED':
            print("STATUS:" + query_execution_status)
            if res_return:
                results = []
                next_token = None
                while True:
                    if next_token:
                        response = client.get_query_results(QueryExecutionId=query_execution_id, NextToken=next_token)
                    else:
                        response = client.get_query_results(QueryExecutionId=query_execution_id)
                    
                    results.extend(response['ResultSet']['Rows'])
                    
                    next_token = response.get('NextToken')
                    if not next_token:
                        break
                response['ResultSet']['Rows'] = results
                return (True,response)
            break
        if query_execution_status == 'FAILED':
            print(query_status)
            query_fail_reason = query_status['QueryExecution']['Status']['StateChangeReason']
            out = f"Query failed while executing in Athena with reason: {query_fail_reason}"
            return (False,out)
        time.sleep(5)


def athena_result_to_df(result):
    columns = [col['Label'] for col in result['ResultSet']['ResultSetMetadata']['ColumnInfo']]
    data = []

    for row in result['ResultSet']['Rows'][1:]:
        # Convert each row to a list of values, replacing None with empty string
        row_data = [col.get('VarCharValue', '') for col in row['Data']]
        data.append(row_data)
    # Create DataFrame
    df = pd.DataFrame(data, columns=columns)
    return df

def run_athena_query(sql):
    res = execute_athen_query(sql)
    if res[0]:
        return athena_result_to_df(res[1])
    else:
        return res[1]
    
def validate_athena_query(sql):
    query = f" EXPLAIN {sql}"
    res = execute_athen_query(query)
    if res[0]:
        return True
    else:
        return False

