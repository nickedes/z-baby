import os
import pymssql
from configparser import ConfigParser


def getValues():
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
        'SELECT * FROM dbo.Subcategory ORDER BY SubCategoryID')
    subcategory = cursor.fetchall()
    conn.close()
    return label, menu, submenu, category, subcategory


def checkLogin(username, password):
    username = "'" + username + "'"
    passwordreal = "'" + password + "'"
    CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

    config = ConfigParser()
    config.read(os.path.join(CURRENT_DIR, 'config.ini'))

    server = config["Database"]["server"]
    user = config["Database"]["user"]
    password = config["Database"]["password"]

    conn = pymssql.connect(server, user, password, "ziiei")

    cursor = conn.cursor()
    cursor.execute(
        'SELECT RoleID FROM dbo.Login WHERE Username = %s AND Password = %s'
        % (username, passwordreal))
    label = cursor.fetchall()
    if not label:
        return None
    else:
        return label[0][0]


def levels():
    CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

    config = ConfigParser()
    config.read(os.path.join(CURRENT_DIR, 'config.ini'))

    server = config["Database"]["server"]
    user = config["Database"]["user"]
    password = config["Database"]["password"]
    conn = pymssql.connect(server, user, password, "ziiei")

    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.Country ORDER BY CountryID')
    country = cursor.fetchall()
    cursor.execute(
        'SELECT * FROM dbo.State ORDER BY StateID')
    state = cursor.fetchall()
    cursor.execute(
        'SELECT * FROM dbo.District ORDER BY DistrictID')
    district = cursor.fetchall()
    cursor.execute(
        'SELECT * FROM dbo.Block ORDER BY BlockID')
    block = cursor.fetchall()
    return country, state, district, block
