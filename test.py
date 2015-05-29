import os
from datetime import datetime
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
# Label (LabelID, LanguageID, LabelType, LabelValue, CreatedBy, CreateDate)


conn.commit()
cursor.execute('SELECT * FROM dbo.Label ORDER BY LabelID')
row = cursor.fetchall()
print(row)
conn.close()
