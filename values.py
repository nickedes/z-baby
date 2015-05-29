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
        'SELECT * FROM dbo.Label where LanguageID=%d ORDER BY LabelID' % lang)
    label = cursor.fetchall()
    cursor.execute(
        'SELECT * FROM dbo.Menu where LanguageID=%d ORDER BY MenuID' % lang)
    menu = cursor.fetchall()
    cursor.execute(
        'SELECT * FROM dbo.SubMenu where LanguageID=%d ORDER BY SubMenuID' % lang)
    submenu = cursor.fetchall()
    cursor.execute(
        'SELECT * FROM dbo.Category where LanguageID=%d ORDER BY CategoryID' % lang)
    category = cursor.fetchall()
    cursor.execute(
        'SELECT * FROM dbo.Label where LanguageID=%d ORDER BY LabelID' % lang)
    subcategory = cursor.fetchall()
    conn.close()
    return label, menu, submenu, category, subcategory
