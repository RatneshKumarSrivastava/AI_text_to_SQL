from schema_reader import create_tables_if_not_exist,get_schema
from llm import creating_prompt
from query_executor import query_execution
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()
database_url = os.getenv("DATABASE_URL")

def main():
    if not database_url:
        raise ValueError("Unable to find DATABASE_URL in .env file")

    #connect with neon sql database
    with psycopg.connect(database_url) as connection:
        with connection.cursor() as cursor:
            print("AI retail data analysis")
            create_tables_if_not_exist(cursor)
            print("Database setup is completed")
            connection.commit()

            llm_str = get_schema(cursor)
            #Ask question
            question = input("\n Ask your business question: ")
            query_sql = creating_prompt(question, llm_str)
            print(
                "\n========== GENERATED SQL =========="
            )
            print(query_sql)
            rows= query_execution(cursor, query_sql)
            for row in rows:
                print(row)

            cursor.close()
            connection.close()

if __name__=="__main__":
    main()