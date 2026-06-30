import pyodbc

try:

    con = pyodbc.connect(

        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=AJITH-RAJA\\SQLEXPRESS;"
        "DATABASE=InventoryDB;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"

    )

    print("Connection Successful")

except Exception as e:

    print(e)