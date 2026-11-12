def query_execution(cursor, query_sql):
    cursor.execute(query_sql)
    rows = cursor.fetchall()
    return rows
