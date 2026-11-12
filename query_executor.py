import pandas as pd
def query_execution(cursor, query_sql):
    cursor.execute(query_sql)
    rows = cursor.fetchall()
    columns = [
        description.name
        for description in cursor.description
    ]
    dataframe = pd.DataFrame(
        rows,
        columns=columns
    )
    return dataframe
