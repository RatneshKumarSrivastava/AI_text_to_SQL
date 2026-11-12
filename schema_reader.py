def create_tables_if_not_exist(cursor):

    # ----------------------------------------------
    # Customers
    # ----------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (

            customer_id BIGSERIAL PRIMARY KEY,

            customer_name VARCHAR(100) NOT NULL,

            city VARCHAR(100),

            state VARCHAR(100),

            customer_segment VARCHAR(50)

        );
    """)

    print("customers table checked")


    # ----------------------------------------------
    # Stores
    # ----------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stores (

            store_id BIGSERIAL PRIMARY KEY,

            store_name VARCHAR(100) NOT NULL,

            city VARCHAR(100),

            state VARCHAR(100),

            region VARCHAR(50)

        );
    """)

    print("stores table checked")


    # ----------------------------------------------
    # Products
    # ----------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (

            product_id BIGSERIAL PRIMARY KEY,

            product_name VARCHAR(150) NOT NULL,

            category VARCHAR(100),

            sub_category VARCHAR(100),

            brand VARCHAR(100),

            unit_price NUMERIC(12,2)

        );
    """)

    print("products table checked")

    # --------------------------------------------------
    # Sales Table
    # --------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (

            sale_id BIGSERIAL PRIMARY KEY,

            customer_id BIGINT
                REFERENCES customers(customer_id),

            store_id BIGINT
                REFERENCES stores(store_id),

            sale_date DATE NOT NULL,

            sales_channel VARCHAR(50),

            payment_method VARCHAR(50),

            total_amount NUMERIC(14,2),

            discount_amount NUMERIC(14,2) DEFAULT 0

        );
    """)

    print("sales table checked")

def get_schema(cursor):
    query_rel = f""" 
    SELECT
            tc.table_name,
            kcu.column_name,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
            AND tc.table_schema = kcu.table_schema
        JOIN information_schema.constraint_column_usage ccu
            ON ccu.constraint_name = tc.constraint_name
            AND ccu.table_schema = tc.table_schema
        WHERE
            tc.constraint_type = 'FOREIGN KEY'
            AND tc.table_schema = 'public'
        ORDER BY
            tc.table_name,
            kcu.column_name
"""
    cursor.execute(query_rel)
    relationship = cursor.fetchall()

    query_col = f"""
    select 
    table_name, 
    column_name, 
    data_type
from information_schema.columns 
    where table_schema='public'
order by 
    table_name,
    ordinal_position
    """
    cursor.execute(query_col)
    columns=cursor.fetchall()

    llm_str = ""
    tbl_name= None
    for col in columns:
        if tbl_name != col[0]:
            llm_str += f"\n Table: {col[0]}\n"
            tbl_name = col[0]
        llm_str += f"\n - {col[1]} : {col[2]}\n"

    llm_str +=f"\n Relationship between tables \n"
    for rel in relationship:
        llm_str += f"\n{rel[0]}.{rel[1]} --> {rel[2]}.{rel[3]}\n"
    return llm_str
