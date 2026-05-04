import os
import json
import boto3
import pg8000.native

bedrock = boto3.client("bedrock-runtime")

def lambda_handler(event, context):
    try:
        # 1. Get user question
        question = event.get("question", "Show all customers")

        # 2. Prompt for SQL generation
        prompt = f"""
You are a SQL generator.

Convert the question into a valid PostgreSQL SQL query.
Return ONLY SQL. No explanation.

Table:
customers(id, name, country, revenue)

Question:
{question}
"""

        # 3. Call Bedrock (Claude)
        response = bedrock.invoke_model(
            modelId=os.environ["BEDROCK_MODEL_ID"],
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 200,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
        )

        result = json.loads(response["body"].read())

        # 4. Extract SQL
        sql_query = result["content"][0]["text"].strip()
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()  

        # Optional safety (basic)
        if not sql_query.lower().startswith("select"):
            return {
                "statusCode": 400,
                "error": "Only SELECT queries allowed",
                "generated_sql": sql_query
            }

        # 5. Connect to Aurora
        conn = pg8000.native.Connection(
            host=os.environ["DB_HOST"],
            database=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            port=int(os.environ["DB_PORT"]),
            ssl_context=True
        )

        # 6. Execute SQL
        rows = conn.run(sql_query)
        conn.close()

        return {
            "statusCode": 200,
            "question": question,
            "sql": sql_query,
            "result": rows
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "error": str(e)
        }
