import os
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
'''
cursor.execute(
    "INSERT INTO dbo.Language VALUES (%s, %d, %s, DEFAULT)",
    ('English', 1, 'lolpol'))

conn.commit()
'''
cursor.execute('SELECT * FROM dbo.Language')
row = cursor.fetchone()
print(row)
conn.close()
