from os import getenv
import pymssql

server = getenv("103.247.98.43:5544")
user = getenv("mssql_licthi")
password = getenv("Mssql@mayank@123")

conn = pymssql.connect(server, user, password, "ziiei")
cursor = conn.cursor()
print conn
