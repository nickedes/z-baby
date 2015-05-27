import pymssql

conn = pymssql.connect(host='103.247.98.43:5544', user='mssql_licthi',
                       password='Mssql@mayank@123', database='ziiei')
cursor = conn.cursor()
cursor.execute(
    "INSERT INTO dbo.Login VALUES (1,'English','nik','admin','lol',DEFAULT)")
conn.commit()

cursor.execute('Select * from dbo.Login')
value = cursor.fetchall()
for row in value:
    print(row)
