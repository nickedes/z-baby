import os
import pymssql
from configparser import ConfigParser


def getValues(lang=1):
    CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

    config = ConfigParser()
    config.read(os.path.join(CURRENT_DIR, 'config.ini'))

    server = config["Database"]["server"]
    user = config["Database"]["user"]
    password = config["Database"]["password"]

    conn = pymssql.connect(server, user, password, "ziiei")

    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.Label ORDER BY LabelID')
    label = cursor.fetchall()
    cursor.execute(
        'SELECT * FROM dbo.Menu ORDER BY MenuID')
    menu = cursor.fetchall()
    cursor.execute(
        'SELECT * FROM dbo.SubMenu ORDER BY SubMenuID')
    submenu = cursor.fetchall()
    cursor.execute(
        'SELECT * FROM dbo.Category ORDER BY CategoryID')
    category = cursor.fetchall()
    cursor.execute(
        'SELECT * FROM dbo.Label ORDER BY LabelID')
    subcategory = cursor.fetchall()
    cursor.execute(
        "SELECT * FROM dbo.Label where LabelType = 'Enquiry'")
    enquiry = cursor.fetchall()
    conn.close()
    return label, menu, submenu, category, subcategory, enquiry
