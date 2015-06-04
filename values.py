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

def gettablelist():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM information_schema.tables')
    val = cursor.fetchall()
    return val

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
    print(ideaid)
    if not ideaid:
        return False
    return True
    conn.close()


def gettablevalues(tablename):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.%s ORDER BY %sID' %(tablename, tablename))
    returnval = cursor.fetchall()
    return returnval


def addUser():
    pass


def addIdea(UserId):
    pass


def benefit():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.Benefit ORDER BY BenefitID')
    benefit = cursor.fetchall()
    conn.close()
    return benefit


def stage():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.Stage ORDER BY StageID')
    stage = cursor.fetchall()
    conn.close()
    return stage
