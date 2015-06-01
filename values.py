import os
import pymssql
from configparser import ConfigParser


def getConnection():
    CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

    config = ConfigParser()
    config.read(os.path.join(CURRENT_DIR, 'config.ini'))

    server = config["Database"]["server"]
    user = config["Database"]["user"]
    password = config["Database"]["password"]
    conn = pymssql.connect(server, user, password, "ziiei")

    return conn

def getValues():
    conn = getConnection()
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
    
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT RoleID, LoginID FROM dbo.Login WHERE Username = %s AND Password = %s'
        % (username, passwordreal))
    label = cursor.fetchall()
    if not label:
        return None
    else:
        return label
    conn.close()


def checkInnovation(userid):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT IdeaID from Idea WHERE LoginID = %d' % userid)
    ideaid = cursor.fetchall()
    print (ideaid)
    if not ideaid:
        return False
    return True 
    conn.close()


def levels():
    conn = getConnection()
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
    conn.close()
    return country, state, district, block
