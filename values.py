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


def insertvalues(name, dob, sch_name, sch_addr, ph, alt_ph, doj, awards,
                 empid, qual, gender, resi_addr, email, desig, subj, block,
                 dist, state, country, cr_by, cr_date):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO dbo.Registration VALUES (%s, %s, %s, %s, %d, %d, %s, %s, %s, %s, %s, %s, %s, %s, %s, %d, %d, %d, %d, %s, %s)', (name, dob, sch_name, sch_addr, ph, alt_ph, doj, awards, empid, qual, gender, resi_addr, email, desig, subj, block, dist, state, country, str(cr_by), cr_date))
        conn.commit()
        # todo: Password Logic
        password = "dummy"
        cursor.execute(
            'SELECT LoginID FROM dbo.Registration WHERE EmployeeID = %s', empid)
        loginid = cursor.fetchall()
        try:
            cursor.execute(
                'INSERT INTO dbo.Login VALUES (%d, %s, %s, %d, %s, %s, %s)', (loginid[0][0], empid, password, 1, "Teacher", str(cr_by), cr_date))
            conn.commit()
            conn.close()
        except:
            return False
    except:
        return False
    return True

def insertIdeaCatSubCat(idea_id, category_id, subcategory_id):
    conn = getConnection()
    cursor = conn.cursor()
    vals = []
    for subcategory in subcategory_id:
        vals.append((idea_id, category_id, subcategory))
    try:
        cursor.executemany('INSERT INTO dbo.IdeaCatSubCat VALUES (%d, %d, %d)', vals)
        conn.commit()
    except:
        return False
    return True

def teacherUnderOperator(loginid):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.Login WHERE CreatedBy = %s AND LoginID <> %d', (str(loginid), loginid))
    teachers = cursor.fetchall()
    conn.close()
    return teachers


def getReg_underoperator(loginid):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.Registration WHERE CreatedBy = %s AND LoginID <> %d', (str(loginid), loginid))
    teachers = cursor.fetchall()
    conn.close()
    return teachers

def checkLogin(username, password):
    username = "'" + username + "'"
    passwordreal = "'" + password + "'"

    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT RoleID, LoginID FROM dbo.Login WHERE Username = %s AND Password = %s'
        % (username, passwordreal))
    label = cursor.fetchall()
    conn.close()
    if not label:
        return None
    else:
        return label


def getIdeaCatSubCat(ideaid):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.IdeaCatSubCat WHERE IdeaID = %d', (ideaid))
    CatSubCats = cursor.fetchall()
    conn.close()
    return CatSubCats


def getMedia(ideaid):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.Media WHERE IdeaID = %d', (ideaid))
    media = cursor.fetchall()
    conn.close()
    return media

def getIdeaInfo(loginid):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.Idea WHERE LoginID = %d', (loginid))
    ideas = cursor.fetchall()
    conn.close()
    return ideas


def checkInnovation(userid):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT IdeaID from Idea WHERE LoginID = %d' % userid)
    ideaid = cursor.fetchall()
    conn.close()
    if not ideaid:
        return False
    return True


def gettablevalues(tablename):
    conn = getConnection()
    cursor = conn.cursor()
    if tablename != 'Registration':
        cursor.execute(
            'SELECT * FROM dbo.%s ORDER BY %sID' % (tablename, tablename))
    elif tablename == "Registration":
        cursor.execute(
            'SELECT * FROM dbo.Registration ORDER BY LoginID')
    returnval = cursor.fetchall()
    conn.close()
    return returnval


def getColumns(tablename):
    conn = getConnection()
    cursor = conn.cursor()
    val = "'dbo." + tablename + "'"
    cursor.execute(
        'select * from sys.all_columns where object_id = OBJECT_ID(%s)' % (val))
    column_list = cursor.fetchall()
    columns = [single_column[1] for single_column in column_list]
    return columns


def getLatestIdea():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 1 * FROM dbo.Idea ORDER BY IdeaID DESC")
    latest_idea = cursor.fetchall()
    if not latest_idea:
        return 0
    return latest_idea[0][0]


def insertIdea(IdeaID, LoginID, title, stage, benefit, desc, resource, support, time, reach, cr_by, cr_date):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO dbo.Idea VALUES (%d, %d, %s, %d, %d, %s, %s, %s, %d, %s, %s, %s)', (IdeaID, LoginID, title, stage, benefit, desc, resource, support, time, reach, cr_by, cr_date))
    conn.commit()
    conn.close()
    return True


def getLatestMedia():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 1 * FROM dbo.Media ORDER BY MediaID DESC")
    latest_Media = cursor.fetchall()
    if not latest_Media:
        return 0
    return latest_Media[0][0]


def insertMedia(MediaID, IdeaID, Mtype, Mvalue, cr_by, cr_date):
    # MediaID, IdeaID, 'image', medias['image'], LoginID, datetime.now()
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
        'INSERT INTO dbo.Media VALUES (%d, %d, %s, %s, %s, %s)', (MediaID, IdeaID, Mtype, Mvalue, cr_by, cr_date))
    except:
        return False
    conn.commit()
    conn.close()
    return True


def getRegisteration_details(LoginID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM dbo.Registration where LoginID = %d", LoginID)
    row = cursor.fetchall()
    return row


def update_register(LoginID, name, dob, sch_name, sch_addr, ph, alt_ph, doj, awards,
                    empid, qual, gender, resi_addr, email, desig, subj, block,
                    dist, state, country):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE dbo.Registration set Name=%s, DateOfBirth=%s, SchoolName=%s, SchoolAddress=%s, PhoneNumber=%d, AlternateNumber=%d, DateOfJoining=%s,Awards=%s,EmployeeID=%s,Qualification=%s,Gender=%s,ResidentialAddress=%s,EmailID=%s,Designation=%s,Subjects=%s,BlockID=%d,DistrictID=%d,StateID=%d,CountryID=%d WHERE LoginID = %d', (name, dob, sch_name, sch_addr, ph, alt_ph, doj, awards,
                                                                                                                                                                                                                                                                                                                                                         empid, qual, gender, resi_addr, email, desig, subj, block,
                                                                                                                                                                                                                                                                                                                                                         dist, state, country, LoginID))
        conn.commit()
        try:
            cursor.execute(
                'UPDATE dbo.Login set Username=%s WHERE LoginID=%d', (empid, LoginID))
            conn.commit()
        except:
            return False
    except:
        return False
    conn.close()
    return True


def getLoginID(Username):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
                'SELECT LoginID FROM dbo.Login WHERE Username=%s', (Username))
    row = cursor.fetchall()
    return row[0][0]


def updateIdea(IdeaID,title, stage_id, benefit_id,description, resource, support, implement_time, reach,cr_date):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE dbo.Idea set title=%s,IdueaTitle=%s,StageID=%d,BenefitID=%d,Description=%s,ResourcesRequired=%s,Support=%s,ImplementTime=%d,CreateDate=%s WHERE IdeaID = %d',(title, stage_id, benefit_id,description, resource, support, implement_time, reach,cr_date,IdeaID))
        conn.commit()
    except:
        return False
    conn.close()
    return True


def updateMedia(IdeaID,Mvalue,Mtype,cr_date):
    # IdeaID, medias['image'], 'image', session['userid'], datetime.now())
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE dbo.Media set MediaValue=%s,CreateDate=%s WHERE IdeaID = %d and MediaType = %s',(Mvalue,cr_date,IdeaID,Mtype))
        conn.commit()
    except:
        return False
    conn.close()
    return True


def updateIdeaCatSubCat(idea_id,category_id, subcategory_id):
    # Todo: Improve
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM dbo.IdeaCatSubCat WHERE IdeaID=%d',(idea_id))
    conn.commit()
    vals = []
    for subcategory in subcategory_id:
        vals.append((idea_id, category_id, subcategory))
    try:
        cursor.executemany('INSERT INTO dbo.IdeaCatSubCat VALUES (%d, %d, %d)', vals)
        conn.commit()
    except:
        return False
    return True