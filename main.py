import os
import psycopg
import streamlit as st
from dotenv import load_dotenv
from schema_reader import (
    create_tables_if_not_exist,
    get_schema
)
from llm import creating_prompt
from query_executor import query_execution
# Load Environment Variables
load_dotenv()
database_url = os.getenv("DATABASE_URL")
# Streamlit Page Configuration
st.set_page_config(
    page_title="AI Retail Data Assistant",
    page_icon="🛒",
    layout="wide"
)
# Main Application
def main():
    # Application Header
    st.title("🛒 AI Retail Data Assistant")

    st.write(
        "Ask questions about your retail data "
        "using simple business language."
    )
    # Validate Database Configuration
    if not database_url:
        st.error(
            "DATABASE_URL is missing from .env file."
        )
        st.stop()
    # Business Question
    question = st.text_input(
        "Ask your business question",
        placeholder="Example: Show total sales by region"
    )
    ask_button = st.button(
        "Ask",
        type="primary"
    )
    # Wait for Ask Button
    if not ask_button:
        return
    # Validate Question
    if not question.strip():
        st.warning(
            "Please enter a business question."
        )
        return
    # Process Business Question
    try:
        with st.spinner(
            "Analyzing your retail data..."
        ):

            # Connect to Neon PostgreSQL
            with psycopg.connect(
                database_url
            ) as connection:

                with connection.cursor() as cursor:
                    # Create Tables
                    create_tables_if_not_exist(
                        cursor
                    )
                    connection.commit()
                    # Get Database Schema
                    schema_str = get_schema(
                        cursor
                    )
                    # Generate SQL using Groq
                    query_sql = creating_prompt(
                        question,
                        schema_str
                    )
                    # Execute Generated SQL
                    result = query_execution(
                        cursor,
                        query_sql
                    )
        # Success Message

        st.success(
            "Analysis completed successfully"
        )
        # Display Result
        st.subheader(
            "📊 Result"
        )
        if result is not None:
            st.dataframe(
                result,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.warning(
                "The query returned no result."
            )
        # Display Generated SQL
        with st.expander(
            "🔍 View Generated SQL"
        ):
            st.code(
                query_sql,
                language="sql"
            )
    # Error Handling
    except Exception as error:
        st.error(
            f"Unable to process your question: {error}"
        )
# Run Application
if __name__ == "__main__":

    main()