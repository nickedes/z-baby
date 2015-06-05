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

def getClient_ID():
    CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

    config = ConfigParser()
    config.read(os.path.join(CURRENT_DIR, 'config.ini'))

    CLIENT_ID = config["Imgur"]["CLIENT_ID"]
    return CLIENT_ID

def gettablelist():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM information_schema.tables')
    val = cursor.fetchall()
    return val

def insertvalues(name, dob, sch_name, sch_addr, ph, alt_ph, doj, awards, empid, qual, gender, resi_addr, email, desig, subj, block, dist, state, country, cr_by, cr_date):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO dbo.Registration VALUES (%s, %s, %s, %s, %d, %d, %s, %s, %s, %s, %s, %s, %s, %s, %s, %d, %d, %d, %d, %s, %s)', (name, dob, sch_name, sch_addr, ph, alt_ph, doj, awards, empid, qual, gender, resi_addr, email, desig, subj, block, dist, state, country, cr_by, cr_date))
    conn.commit()
    conn.close()
    return True


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
    if tablename != 'Register':
        cursor.execute(
            'SELECT * FROM dbo.%s ORDER BY %sID' %(tablename, tablename))
    elif tablename =="Register":
        cursor.execute(
            'SELECT * FROM dbo.Register ORDER BY LoginID')
    returnval = cursor.fetchall()
    conn.close()
    return returnval

def getColumns(tablename):
    val = "'dbo." + tablename + "'"
    cursor.execute('select * from sys.all_columns where object_id = OBJECT_ID(%s)' %(val))
    column_list = cursor.fetchall()
    columns = [single_column[1] for single_column in column_list]
    return columns

def addUser():
    pass


def addIdea(UserId):
    pass
