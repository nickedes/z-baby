import os
import datetime
import pymssql
from configparser import ConfigParser

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

config = ConfigParser()
config.read(os.path.join(CURRENT_DIR, 'config.ini'))

server = config["Database"]["server"]
user = config["Database"]["user"]
password = config["Database"]["password"]

conn = pymssql.connect(server, user, password, "ziiei")
cursor = conn.cursor()

cursor.execute(
    "INSERT INTO dbo.Country VALUES (%d, %d, %s, %s, %s)",
    (1, 1, 'India', 'admin', str(datetime.datetime.now())))

conn.commit()

cursor.execute('SELECT * FROM dbo.Country')
row = cursor.fetchone()
print(row)
conn.close()
