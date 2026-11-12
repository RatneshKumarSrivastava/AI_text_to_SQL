# 🛒 AI-Powered Retail Text-to-SQL

## 📌 Overview

**AI-Powered Retail Text-to-SQL** is a Python-based project that allows non-technical business users to query retail data using simple natural-language questions instead of writing SQL.

The application:

1. Connects to a PostgreSQL database hosted on Neon.
2. Dynamically reads tables, columns, data types, and foreign-key relationships.
3. Accepts a natural-language business question.
4. Sends the database schema and question to an LLM using Groq.
5. Generates PostgreSQL SQL automatically.
6. Executes the generated query against PostgreSQL.
7. Returns the result to the user.

---

## 🎯 Business Problem

Business users frequently depend on Data Engineers and Data Analysts for relatively simple questions such as:

- How many customers do we have?
- What are our total sales?
- Which region generated the highest sales?
- Who are our top customers?
- Which store generated the most revenue?
- How many premium customers do we have?

Normally, answering these questions requires someone who understands SQL.

The goal of this project is to provide a natural-language interface between business users and structured enterprise data.

For example, a user can ask:

```text
Show top 5 customers by total sales
```

The application can generate:

```sql
SELECT
    c.customer_name,
    SUM(s.total_amount) AS total_sales
FROM sales AS s
JOIN customers AS c
    ON s.customer_id = c.customer_id
GROUP BY
    c.customer_name
ORDER BY
    total_sales DESC
LIMIT 5;
```

---

# 🏗️ Architecture

```text
Business User
     │
     │
     │ Natural Language Question
     │
     ▼
Python Application
     │
     ▼
PostgreSQL Schema Reader
     │
     ├── Tables
     ├── Columns
     ├── Data Types
     └── Foreign Key Relationships
     │
     ▼
Prompt Creation
     │
     │
     ├── Business Question
     ├── Database Schema
     ├── Table Relationships
     └── SQL Generation Rules
     │
     ▼
Groq LLM
     │
     ▼
Generated PostgreSQL Query
     │
     ▼
Query Executor
     │
     ▼
Neon PostgreSQL
     │
     ▼
Query Result
     │
     ▼
Business User
```

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| PostgreSQL | Relational database |
| Neon | Serverless PostgreSQL hosting |
| Groq | LLM inference API |
| GPT-OSS | LLM used for Text-to-SQL generation |
| Psycopg | Python PostgreSQL connectivity |
| python-dotenv | Environment variable management |
| Pandas | Query-result processing |
| Git | Source control |
| GitHub | Code repository |

---

# 📁 Project Structure

```text
AI_text_to_SQL/
│
├── main.py
│
├── schema_reader.py
│
├── llm.py
│
├── query_executor.py
│
├── requirements.txt
│
├── .env.example
│
├── .gitignore
│
└── README.md
```

---

# 📄 File Description

## `main.py`

Main entry point and controller of the application.

Responsibilities:

- Load environment variables
- Connect to Neon PostgreSQL
- Create/check required tables
- Read database schema
- Accept business questions
- Call the LLM
- Receive generated SQL
- Execute the query
- Display results

---

## `schema_reader.py`

Responsible for database schema and metadata management.

The module:

- Creates required retail tables if they do not exist
- Reads table names
- Reads column names
- Reads column data types
- Identifies foreign-key relationships
- Creates schema context for the LLM

Example schema context:

```text
Table: customers
- customer_id: bigint
- customer_name: character varying
- city: character varying
- state: character varying
- customer_segment: character varying
```

Example relationship:

```text
sales.customer_id -> customers.customer_id
```

## Author
### Ratnesh Srivastava

Data Engineering | Cloud Data Platforms | Python | SQL | Generative AI | AI-powered Data Engineering solutions
https://www.linkedin.com/in/ratnesh-srivastava-702b61a8/
