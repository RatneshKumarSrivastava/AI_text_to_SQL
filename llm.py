import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')
if not groq_api_key:
    ValueError("unable to connect groq")

#create groq client
client = Groq(api_key=groq_api_key)

def creating_prompt(question, schema_str):
    prompt = f"""
    you are expert in data engineering.
    you have to convert question into postgres sql query.
    all the details related to tables, columns and there relationship(foreign keys)
    are available below:
    {schema_str}    
    
    Business question is :
    {question}
    
    There are some rules do's and don't do:
    Do's:
    1. Generate only select query.
    2. Use only those tables which are present in given Database.
    3. return only postgres sql query.
    
    Don't do :
    1. never generate INSERT,UPDATE, DELETE, DROP, ALTER, TRUNCATE , CREATE query.
    2. Do not invent table
    3. Do not invent records , columns.
    4. Do not add Markdown.
    5. Do not use ```sql.

"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content":
                    "You are an expert PostgreSQL data analyst."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )
    sql = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )
    return sql