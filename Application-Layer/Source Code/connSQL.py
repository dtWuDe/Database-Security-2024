import pyodbc

def Connect(Server: str, Database: str, UID: str, PWD: str):
    # Establish a connection
    conn = pyodbc.connect(
        "Driver={SQL Server};"
        f"Server={Server};"
        f"Database={Database};"
        f"UID={UID};"
        f"PWD={PWD};"
    )

    # Create a cursor
    cursor = conn.cursor()

    return conn, cursor

def Disconnect(conn, cursor):
    # Close the cursor and connection
    cursor.close()
    conn.close()