import requests
import os
import pyodbc
import ConfigParser
from datetime import datetime
from random import randint


def getConnection():
	config = ConfigParser.RawConfigParser()
	config.read('config.ini')

	server = config.get('Database', 'server')
	user = config.get('Database', 'user')
	password = config.get('Database', 'password')

	connection_string = 'DRIVER={SQL Server};SERVER=%s;DATABASE=ziiei;UID=%s;PWD=%s' % (server, user, password)

	cnxn = pyodbc.connect(connection_string)
	return cnxn


def getClient_ID():
    config = ConfigParser.RawConfigParser()
    config.read('config.ini')

    CLIENT_ID = config.get('Imgur','CLIENT_ID')
    return CLIENT_ID


def getVimeo():
    config = ConfigParser.RawConfigParser()
    config.read('config.ini')
    token = config.get('Vimeo','token')
    secret= config.get('Vimeo','secret')
    Client_Identifier= config.get('Vimeo','Client_Identifier')
    return VimeoClient(token=token,key=Client_Identifier,secret=secret)


def sendPassword(msg, phone):
    config = ConfigParser.RawConfigParser()
    config.read('config.ini')
    url = config.get('Sms', 'url')
    usr = config.get('Sms', 'usr')
    passwd = config.get('Sms', 'pass')
    sid = config.get('Sms', 'sid')
    mt = config.get('Sms', 'mt')
    try:
        r = requests.post(url=url, data={'usr': usr,'pass':passwd,'msisdn':phone,
            'msg':msg,'sid':sid,'mt':mt})
        return True
    except:
        return False


def gettablelist():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM information_schema.tables')
    val = cursor.fetchall()
    return val


def getPassword():
    return "%0.6d" % randint(0,999999)


def insertvalues(name, dob, sch_name, sch_addr, ph, alt_ph, doj, awards,
                 empid, qual, gender, resi_addr, email, desig, subj, block,
                 dist, state, country, cr_by, cr_date):
    conn_reg = getConnection()
    cursor = conn_reg.cursor()
    # try:
    vals = (name, dob, sch_name, sch_addr, ph, alt_ph, doj, awards, empid, qual, gender, resi_addr, email, desig, subj, block, dist, state, country, str(cr_by), cr_date)
    cursor.execute(
        'INSERT INTO dbo.Registration VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', vals)
    conn_reg.commit()

    # Password - A 6 digit Random no.
    password = getPassword()
    # Send SMS to teacher, Username and Password.
    # Username is Empid
    msg = 'Username:'+ empid + '\n' + 'Password:' + password
    if sendPassword(msg,ph):
        print 'Sms Sent'
    else:
        print 'Sms failed'
    cursor.execute(
        'SELECT LoginID FROM dbo.Registration WHERE EmployeeID = ?', empid)
    loginid = cursor.fetchall()
    print loginid,empid,password,1,"teacher",str(cr_by), cr_date
    # cursor.execute('INSERT INTO dbo.Login VALUES (?, ?, ?, ?, ?, ?, ?)', (loginid[0][0], empid, password, 1, "Teacher", cr_by, cr_date))
    # conn_reg.commit()
    if createLogin(loginid[0][0], empid, password, 1, "Teacher", cr_by, cr_date):
        print 'Login created'
    else:
        print 'Login Failed'
    conn_reg.close()
    # conn.close()
    return True


def insertIdeaCatSubCat(idea_id, category_id, subcategory_id,cr_by, cr_date):
    conn = getConnection()
    cursor = conn.cursor()
    vals = []
    for subcategory in subcategory_id:
        vals.append((idea_id, category_id, subcategory, cr_by, cr_date))
    try:
        cursor.executemany(
            'INSERT INTO dbo.IdeaCatSubCat VALUES (?, ?, ?, ?, ?)', vals)
        conn.commit()
    except:
        return False
    return True


def teacherUnderOperator(loginid):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.Login WHERE CreatedBy = ? AND LoginID <> ?', (str(loginid), loginid))
    teachers = cursor.fetchall()
    conn.close()
    return teachers


def getReg_underoperator(loginid):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.Registration WHERE CreatedBy = ? AND LoginID <> ?', (str(loginid), loginid))
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
        'SELECT IdeaID,CategoryID,SubCategoryID FROM dbo.IdeaCatSubCat WHERE IdeaID = ?', (ideaid))
    CatSubCats = cursor.fetchall()
    conn.close()
    return CatSubCats


def getMedia(ideaid):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.Media WHERE IdeaID = ?', (ideaid))
    media = cursor.fetchall()
    conn.close()
    return media


def getIdeaInfo(loginid):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.Idea WHERE LoginID = ?', (loginid))
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


def insertCat(CategoryID, CategoryValue, CreatedBy):
    conn = getConnection()
    cursor = conn.cursor()
    CreateDate = datetime.now()
    LangIDs = getLangIDs()
    try:
        for LanguageID in LangIDs:
            cursor.execute(
                'INSERT INTO dbo.Category VALUES (?, ?, ?, ?, ?)', (LanguageID, CategoryID, CategoryValue, CreatedBy, CreateDate))
            conn.commit()
    except:
        return False
    return True


def insertSubCat(CategoryID, SubCategoryID, SubValue, CreatedBy):
    conn = getConnection()
    cursor = conn.cursor()
    CreateDate = datetime.now()
    LangIDs = getLangIDs()
    # SubCategory (LanguageID, CategoryID, SubCategoryID, SubCategoryValue, CreatedBy, CreateDate)
    try:
        for LanguageID in LangIDs:
            cursor.execute(
                'INSERT INTO dbo.SubCategory VALUES (?, ?, ?, ?, ?, ?)', (LanguageID, CategoryID, SubCategoryID, SubValue, CreatedBy, CreateDate))
            conn.commit()
    except:
        return False
    return True


def gettablevalues(tablename):
    conn = getConnection()
    cursor = conn.cursor()
    if tablename != 'Registration' and tablename != 'IdeaCatSubCat':
        cursor.execute(
            'SELECT * FROM dbo.%s ORDER BY %sID' % (tablename, tablename))
    elif tablename == "Registration":
        cursor.execute(
            'SELECT * FROM dbo.Registration ORDER BY LoginID')
    elif tablename == "IdeaCatSubCat":
        cursor.execute(
            'SELECT * FROM dbo.IdeaCatSubCat ORDER BY IdeaID')
    returnval = cursor.fetchall()
    conn.close()
    return returnval


def insertMenu(menuvalues):
    conn = getConnection()
    cursor = conn.cursor()
    # try:
    cursor.execute(
            'INSERT INTO dbo.Menu VALUES (?, ?, ?, ?, ?, ?, ?, ?)', menuvalues)
    # except:
    #     return False
    conn.commit()
    return True


def insertCountry(CountryID, CountryName, CreatedBy):
    conn = getConnection()
    cursor = conn.cursor()
    CreateDate = datetime.now()
    LangIDs = getLangIDs()
    try:
        for LanguageID in LangIDs:    
            cursor.execute(
                'INSERT INTO dbo.Country VALUES (?, ?, ?, ?, ?)', (LanguageID, CountryID, CountryName, CreatedBy, CreateDate))
            conn.commit()
    except:
        return False
    return True
    # State (LanguageID, CountryID, StateID, StateName, CreatedBy, CreateDate)


def insertState(CountryID, StateID, StateName, CreatedBy):
    conn = getConnection()
    cursor = conn.cursor()
    CreateDate = datetime.now()
    LangIDs = getLangIDs()
    try:
        for LanguageID in LangIDs:
            cursor.execute(
                'INSERT INTO dbo.State VALUES (?, ?, ?, ?, ?, ?)', (LanguageID, CountryID, StateID, StateName, CreatedBy, CreateDate))
            conn.commit()
    except:
        return False
    return True


def insertSubMenu(submenuvalues):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO dbo.SubMenu VALUES (?, ?, ?, ?, ?, ?, ?, ?)', submenuvalues)
    except:
        return False
    conn.commit()
    return True


def insertLabel(labelvalues):
    conn = getConnection()
    cursor = conn.cursor()
    # try:
    cursor.execute(
        'INSERT INTO dbo.Label VALUES (?, ?, ?, ?, ?, ?, ?, ?)', labelvalues)
    # except:
    #     return False
    conn.commit()
    return True


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
        'INSERT INTO dbo.Idea VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (IdeaID, LoginID, title, stage, benefit, desc, resource, support, time, reach, cr_by, cr_date))
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
    # try:
    cursor.execute(
            'INSERT INTO dbo.Media VALUES (?, ?, ?, ?, ?, ?)', (MediaID, IdeaID, Mtype, Mvalue, cr_by, cr_date))
    # except:
    #     return False
    conn.commit()
    conn.close()
    return True


def getRegisteration_details(LoginID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM dbo.Registration where LoginID = ?", LoginID)
    row = cursor.fetchall()
    return row


def update_register(LoginID, name, dob, sch_name, sch_addr, ph, alt_ph, doj, awards,
                    empid, qual, gender, resi_addr, email, desig, subj, block,
                    dist, state, country):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE dbo.Registration set Name=?, DateOfBirth=?, SchoolName=?, SchoolAddress=?, PhoneNumber=?, AlternateNumber=?, DateOfJoining=?,Awards=?,EmployeeID=?,Qualification=?,Gender=?,ResidentialAddress=?,EmailID=?,Designation=?,Subjects=?,BlockID=?,DistrictID=?,StateID=?,CountryID=? WHERE LoginID = ?', name, dob, sch_name, sch_addr, ph, alt_ph, doj, awards,
                                                                                                                                                                                                                                                                                                                                                         empid, qual, gender, resi_addr, email, desig, subj, block,
                                                                                                                                                                                                                                                                                                                                                         dist, state, country, int(LoginID))
        conn.commit()
        try:
            cursor.execute('UPDATE dbo.Login set Username=? WHERE LoginID=?', empid, LoginID)
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
        'SELECT LoginID FROM dbo.Login WHERE Username=?', (Username))
    row = cursor.fetchall()
    return row[0][0]


def updateIdea(IdeaID, title, stage_id, benefit_id, description, resource, support, implement_time, reach):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE dbo.Idea set IdeaTitle=?,StageID=?,BenefitID=?,Description=?,ResourcesRequired=?,Support=?,ImplementTime=?, Reach=? WHERE IdeaID = ?', (title, stage_id, benefit_id, description, resource, support, implement_time, reach, IdeaID))
        conn.commit()
    except:
        return False
    conn.close()
    return True


def updateMedia(IdeaID, Mvalue, Mtype, cr_date, MediaID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE dbo.Media set MediaValue=?,CreateDate=? WHERE MediaID = ? and IdeaID = ? and MediaType = ?', (Mvalue, cr_date, MediaID, IdeaID, Mtype))
        conn.commit()
    except:
        return False
    conn.close()
    return True


def updateLabel(LabelID, LabelValue, LanguageID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE dbo.Label set LabelValue=? WHERE LabelID = ? and LanguageID = ?', (LabelValue, LabelID, LanguageID))
        conn.commit()
    except:
        return False
    conn.close()
    return True


def updateIdeaCatSubCat(idea_id, category_id, subcategory_id, cr_by, cr_date):
    # Todo: Improve
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM dbo.IdeaCatSubCat WHERE IdeaID=?', (idea_id))
    conn.commit()
    vals = []
    for subcategory in subcategory_id:
        vals.append((idea_id, category_id, subcategory, cr_by, cr_date))
    try:
        cursor.executemany(
            'INSERT INTO dbo.IdeaCatSubCat VALUES (?, ?, ?, ?, ?)', vals)
        conn.commit()
    except:
        return False
    return True


def getIdeaUnderOperator(LoginID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dbo.Idea WHERE CreatedBy = ?', str(LoginID))
    return cursor.fetchall()


def updateCat(LangID, CategoryID, CategoryValue):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE dbo.Category set CategoryValue = ? WHERE CategoryID = ? and LanguageID = ?', (CategoryValue, CategoryID, LangID))
    except:
        return False
    conn.commit()
    return True


def updateSubCat(LangID, CategoryID, SubCategoryID, CategoryValue):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE dbo.SubCategory set SubCategoryValue = ? WHERE CategoryID = ? and SubCategoryID = ? and LanguageID = ?',
                       (CategoryValue, CategoryID, SubCategoryID, LangID))
    except:
        return False
    conn.commit()
    return True


def updateMenu(LangID, MenuID, FormName):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE dbo.Menu set FormName = ? WHERE MenuID = ? and LanguageID = ?', (FormName, MenuID, LangID))
    except:
        return False
    conn.commit()
    return True


def updateSubMenu(LanguageID, MenuID, SubMenuID, MenuValue):
    conn = getConnection()
    cursor = conn.cursor()
    # try:
    cursor.execute('UPDATE dbo.SubMenu set FormName = ? WHERE MenuID = ? and SubMenuID = ? and LanguageID = ?',
                       (MenuValue, MenuID, SubMenuID, LanguageID))
    # except:
    #     return False
    conn.commit()
    return True


def updateCountry(LangID, CountryID, CountryName):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE dbo.Country set CountryName = ? WHERE CountryID = ? and LanguageID = ?', (CountryName, CountryID, LangID))
    except:
        return False
    conn.commit()
    return True


def updateState(LangID, CountryID, StateID, StateName):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE dbo.State set StateName = ? WHERE LanguageID = ? and CountryID = ? and StateID = ?',
                       (StateName, LangID, CountryID, StateID))
    except:
        return False
    conn.commit()
    return True


def updateDistrict(LangID, CountryID, StateID, DistrictID, DistrictName):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE dbo.District set DistrictName = ? WHERE LanguageID = ? and CountryID = ? and StateID = ? and DistrictID = ?',
                       (DistrictName, LangID, CountryID, StateID, DistrictID))
    except:
        return False
    conn.commit()
    return True


def updateBlock(LangID, CountryID, StateID, DistrictID, BlockID, DistrictName):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE dbo.Block set BlockName = ? WHERE LanguageID = ? and CountryID = ? and StateID = ? and DistrictID = ? and BlockID =?',
                       (DistrictName, LangID, CountryID, StateID, DistrictID, BlockID))
    except:
        return False
    conn.commit()
    return True


def SupdateMedia(MediaID, IdeaID, value, Mtype):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE dbo.Media set IdeaID = ?, MediaValue = ?, MediaType = ? WHERE MediaID = ?',
                       (IdeaID, value, Mtype, MediaID))
    except:
        return False
    conn.commit()
    return True


def NoIdea(IdeaID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dbo.Idea WHERE IdeaID=?', IdeaID)
    if cursor.fetchall() == []:
        return True
    return False


def deleteMedia(MediaID, IdeaID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM dbo.Media WHERE MediaID=? and IdeaID=?', (MediaID, IdeaID))
    except:
        return False
    conn.commit()
    return True


def CheckCountry(CountryID):
    # Check if there is a state for this Country.
    # If yes then NO DELETION!
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dbo.State WHERE CountryID=?', CountryID)
    if cursor.fetchall():
        return True
    return False


def deleteCountry(LangID, CountryID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM dbo.Country WHERE CountryID=? and LanguageID=?', (CountryID, LangID))
    except:
        return False
    conn.commit()
    return True


def getCountryID():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(CountryID) FROM dbo.Country")
    top = cursor.fetchall()
    if not top[0][0]:
        return 0
    return top[0][0]


def getStateID(CountryID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(StateID) FROM dbo.State WHERE CountryID = ?", (CountryID))
    top = cursor.fetchall()
    if not top[0][0]:
        return 0
    return top[0][0]


def CheckState(StateID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dbo.District WHERE StateID=?', StateID)
    if cursor.fetchall():
        return True
    return False


def deleteState(LangID, CountryID, StateID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM dbo.State WHERE CountryID=? and LanguageID=? and StateID=?',
            (CountryID, LangID, StateID))
    except:
        return False
    conn.commit()
    return True


def CheckDistrict(DistrictID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dbo.Block WHERE DistrictID=?', DistrictID)
    if cursor.fetchall():
        return True
    return False


def deleteDistrict(LangID, CountryID, StateID, DistrictID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM dbo.District WHERE CountryID=? and LanguageID=? and StateID=? and DistrictID=?',
            (CountryID, LangID, StateID, DistrictID))
    except:
        return False
    conn.commit()
    return True


def NoCountry(CountryID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dbo.Country WHERE CountryID=?', CountryID)
    if cursor.fetchall() == []:
        return True
    return False


def NoState(StateID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dbo.State WHERE StateID=?', StateID)
    if cursor.fetchall() == []:
        return True
    return False


def getDistrictID(CountryID, StateID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(DistrictID) FROM dbo.District WHERE CountryID = ? and StateID = ?", (CountryID, StateID))
    top = cursor.fetchall()
    if not top[0][0]:
        return 0
    return top[0][0]


def NoDistrict(DistrictID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.District WHERE DistrictID=?', DistrictID)
    if cursor.fetchall() == []:
        return True
    return False


def insertDistrict(CountryID, StateID, DistrictID, DistrictName, CreatedBy):
    conn = getConnection()
    cursor = conn.cursor()
    CreateDate = datetime.now()
    LangIDs = getLangIDs()
    try:
        for LanguageID in LangIDs:
            cursor.execute(
                'INSERT INTO dbo.District VALUES (?, ?, ?, ?, ?, ?, ?)', (LanguageID, CountryID, StateID, DistrictID, DistrictName, CreatedBy, CreateDate))
            conn.commit()
    except:
        return False
    return True


def deleteBlock(LangID, CountryID, StateID, DistrictID, BlockID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM dbo.Block WHERE CountryID=? and LanguageID=? and StateID=? and DistrictID=? and BlockID=?',
            (CountryID, LangID, StateID, DistrictID, BlockID))
    except:
        return False
    conn.commit()
    return True


def getBlockID(CountryID, StateID, DistrictID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(BlockID) FROM dbo.Block WHERE CountryID = ? and StateID = ? \
         and DistrictID = ?", (CountryID, StateID, DistrictID))
    top = cursor.fetchall()
    if not top[0][0]:
        return 0
    return top[0][0]


def insertBlock(CountryID, StateID, DistrictID, BlockID, BlockName, CreatedBy):
    conn = getConnection()
    cursor = conn.cursor()
    CreateDate = datetime.now()
    LangIDs = getLangIDs()
    try:
        for LanguageID in LangIDs:
            cursor.execute(
                'INSERT INTO dbo.Block VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (LanguageID, CountryID, StateID, DistrictID, BlockID, BlockName, CreatedBy, CreateDate))
            conn.commit()
    except:
        return False
    return True


def getCatID():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT max(CategoryID) FROM dbo.Category")
    top = cursor.fetchall()
    if not top[0][0]:
        return 0
    return top[0][0]


def CheckCategory(CategoryID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.SubCategory WHERE CategoryID=?', CategoryID)
    if cursor.fetchall():
        return True
    return False


def NoCategory(CategoryID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.Category WHERE CategoryID=?', CategoryID)
    if cursor.fetchall() == []:
        return True
    return False


def getSubCatID(LangID, CategoryID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(SubCategoryID) FROM dbo.SubCategory WHERE LanguageID = ? and CategoryID = ?", (LangID, CategoryID))
    top = cursor.fetchall()
    if not top[0][0]:
        return 0
    return top[0][0]


def deleteCategory(LangID, CategoryID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM dbo.Category WHERE CategoryID=? and LanguageID=?', (CategoryID, LangID))
    except:
        return False
    conn.commit()
    return True


def deleteSub(LangID, CatID, SubCatID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM dbo.SubCategory WHERE LanguageID=?  and CategoryID=? and SubCategoryID=?',
            (LangID, CatID, SubCatID))
    except:
        return False
    conn.commit()
    return True


def updateStage(LangID, StageID, StageName):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE dbo.Stage set StageValue = ? WHERE StageID = ? and LanguageID = ?', (StageName, StageID, LangID))
    except:
        return False
    conn.commit()
    return True


def deleteStage(LangID, StageID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM dbo.Stage WHERE StageID=? and LanguageID=?', (StageID, LangID))
    except:
        return False
    conn.commit()
    return True


def getStageID():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(StageID) FROM dbo.Stage")
    top = cursor.fetchall()
    if not top[0][0]:
        return 0
    return top[0][0]


def insertStage(LanguageID, StageID, value, CreatedBy):
    conn = getConnection()
    cursor = conn.cursor()
    CreateDate = datetime.now()
    LangIDs = getLangIDs()
    try:
        for LanguageID in LangIDs:
            cursor.execute(
                'INSERT INTO dbo.Stage VALUES (?, ?, ?, ?, ?)', (LanguageID, StageID, value, CreatedBy, CreateDate))
            conn.commit()
    except:
        return False
    return True


def insertLang(name, CreatedBy):
    conn = getConnection()
    cursor = conn.cursor()

    labelvals = gettablevalues('Label')
    menuvals = gettablevalues('Menu')
    submenuvals = gettablevalues('SubMenu')
    benefitvals = gettablevalues('Benefit')
    stagevals = gettablevalues('Stage')
    blockvals = gettablevalues('Block')
    districtvals = gettablevalues('District')
    statevals = gettablevalues('State')
    countryvals = gettablevalues('Country')
    categoryvals = gettablevalues('Category')
    subcategoryvals = gettablevalues('SubCategory')

    finallabel = []
    finalmenu = []
    finalsubmenu = []
    finalbenefit = []
    finalstage = []
    finalblock = []
    finaldistrict = []
    finalstate = []
    finalcountry = []
    finalcategory = []
    finalsubcategory = []

    CreateDate = datetime.now()

    cursor.execute(
        'INSERT INTO dbo.Language VALUES (?, ?, ?, ?)', (name, 0, CreatedBy, CreateDate))
    conn.commit()

    lang_id = getLangID()

    for label in labelvals:
        if label[1] == 1:
            labellist = list(label)
            labellist[1] = lang_id
            labellist[6] = CreatedBy
            labellist[7] = datetime.now()
            labeltuple = tuple(labellist)
            finallabel.append(labeltuple)

    for menu in menuvals:
        if menu[0] == 1:
            menulist = list(menu)
            menulist[0] = lang_id
            menulist[6] = CreatedBy
            menulist[7] = datetime.now()
            menutuple = tuple(menulist)
            finalmenu.append(menutuple)
    for submenu in submenuvals:
        if submenu[0] == 1:
            submenulist = list(submenu)
            submenulist[0] = lang_id
            submenulist[6] = CreatedBy
            submenulist[7] = datetime.now()
            submenutuple = tuple(submenulist)
            finalsubmenu.append(submenutuple)
    for benefit in benefitvals:
        if benefit[0] == 1:
            benefitlist = list(benefit)
            benefitlist[0] = lang_id
            benefitlist[3] = CreatedBy
            benefitlist[4] = datetime.now()
            benefittuple = tuple(benefitlist)
            finalbenefit.append(benefittuple)
    for stage in stagevals:
        if stage[0] == 1:
            stagelist = list(stage)
            stagelist[0] = lang_id
            stagelist[3] = CreatedBy
            stagelist[4] = datetime.now()
            stagetuple = tuple(stagelist)
            finalstage.append(stagetuple)
    for block in blockvals:
        if block[0] == 1:
            blocklist = list(block)
            blocklist[0] = lang_id
            blocklist[6] = CreatedBy
            blocklist[7] = datetime.now()
            blocktuple = tuple(blocklist)
            finalblock.append(blocktuple)
    for district in districtvals:
        if district[0] == 1:
            districtlist = list(district)
            districtlist[0] = lang_id
            districtlist[5] = CreatedBy
            districtlist[6] = datetime.now()
            districttuple = tuple(districtlist)
            finaldistrict.append(districttuple)
    for state in statevals:
        if state[0] == 1:
            statelist = list(state)
            statelist[0] = lang_id
            statelist[4] = CreatedBy
            statelist[5] = datetime.now()
            statetuple = tuple(statelist)
            finalstate.append(statetuple)
    for country in countryvals:
        if country[0] == 1:
            countrylist = list(country)
            countrylist[0] = lang_id
            countrylist[3] = CreatedBy
            countrylist[4] = datetime.now()
            countrytuple = tuple(countrylist)
            finalcountry.append(countrytuple)
    for category in categoryvals:
        if category[0] == 1:
            categorylist = list(category)
            categorylist[0] = lang_id
            categorylist[3] = CreatedBy
            categorylist[4] = datetime.now()
            categorytuple = tuple(categorylist)
            finalcategory.append(categorytuple)
    for subcategory in subcategoryvals:
        if subcategory[0] == 1:
            subcategorylist = list(subcategory)
            subcategorylist[0] = lang_id
            subcategorylist[4] = CreatedBy
            subcategorylist[5] = datetime.now()
            subcategorytuple = tuple(subcategorylist)
            finalsubcategory.append(subcategorytuple)

    cursor.executemany(
        'INSERT INTO dbo.Label VALUES (?, ?, ?, ?, ?, ?, ?, ?)', finallabel)
    conn.commit()
    cursor.executemany(
        'INSERT INTO dbo.Menu VALUES (?, ?, ?, ?, ?, ?, ?, ?)', finalmenu)
    conn.commit()
    cursor.executemany(
        'INSERT INTO dbo.SubMenu VALUES (?, ?, ?, ?, ?, ?, ?, ?)', finalsubmenu)
    conn.commit()
    cursor.executemany(
        'INSERT INTO dbo.Country VALUES (?, ?, ?, ?, ?)', finalcountry)
    conn.commit()
    cursor.executemany(
        'INSERT INTO dbo.State VALUES (?, ?, ?, ?, ?, ?)', finalstate)
    conn.commit()
    cursor.executemany(
        'INSERT INTO dbo.District VALUES (?, ?, ?, ?, ?, ?, ?)', finaldistrict)
    conn.commit()
    cursor.executemany(
        'INSERT INTO dbo.Block VALUES (?, ?, ?, ?, ?, ?, ?, ?)', finalblock)
    conn.commit()
    cursor.executemany(
        'INSERT INTO dbo.Benefit VALUES (?, ?, ?, ?, ?)', finalbenefit)
    conn.commit()
    cursor.executemany(
        'INSERT INTO dbo.Stage VALUES (?, ?, ?, ?, ?)', finalstage)
    conn.commit()
    cursor.executemany(
        'INSERT INTO dbo.Category VALUES (?, ?, ?, ?, ?)', finalcategory)
    conn.commit()
    cursor.executemany(
        'INSERT INTO dbo.SubCategory VALUES (?, ?, ?, ?, ?, ?)', finalsubcategory)
    conn.commit()
    return True


def getLangID():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(LanguageID) FROM dbo.Language ")
    top = cursor.fetchall()
    if not top[0][0]:
        return 0
    return top[0][0]


def updateLang(LangID, name, masterlang):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        if masterlang == 'True':
            masterlang = 1
        elif masterlang == 'False':
            masterlang = 0
        else:
            return False
        cursor.execute(
            'UPDATE dbo.Language set LanguageName = ?,MasterLanguage=? WHERE LanguageID = ?', (name, masterlang, LangID))
    except:
        return False
    conn.commit()
    return True


def checkLang(LangID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dbo.Menu WHERE LanguageID=?', LangID)
    if cursor.fetchall():
        return True
    cursor.execute('SELECT * FROM dbo.Benefit WHERE LanguageID=?', LangID)
    if cursor.fetchall():
        return True
    cursor.execute('SELECT * FROM dbo.Stage WHERE LanguageID=?', LangID)
    if cursor.fetchall():
        return True
    cursor.execute('SELECT * FROM dbo.Category WHERE LanguageID=?', LangID)
    if cursor.fetchall():
        return True
    cursor.execute('SELECT * FROM dbo.Country WHERE LanguageID=?', LangID)
    if cursor.fetchall():
        return True
    cursor.execute('SELECT * FROM dbo.Label WHERE LanguageID=?', LangID)
    if cursor.fetchall():
        return True
    return False


def deleteLang(LangID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM dbo.Language WHERE LanguageID=?', LangID)
    except:
        return False
    conn.commit()
    return True


def updateBenefit(LangID, BenefitID, value):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE dbo.Benefit set BenefitValue = ? WHERE BenefitID = ? and LanguageID = ?', (value, BenefitID, LangID))
    except:
        return False
    conn.commit()
    return True


def deleteBenefit(LangID, BenefitID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM dbo.Benefit WHERE BenefitID=? and LanguageID=?', (BenefitID, LangID))
    except:
        return False
    conn.commit()
    return True


def getBenefitID():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(BenefitID) FROM dbo.Benefit")
    top = cursor.fetchall()
    if not top[0][0]:
        return 0
    return top[0][0]


def insertBenefit(LanguageID, BenefitID, value, CreatedBy):
    conn = getConnection()
    cursor = conn.cursor()
    CreateDate = datetime.now()
    LangIDs = getLangIDs()
    try:
        for LanguageID in LangIDs:
            cursor.execute(
                'INSERT INTO dbo.Benefit VALUES (?, ?, ?, ?, ?)', (LanguageID, BenefitID, value, CreatedBy, CreateDate))
            conn.commit()
    except:
        return False
    return True


def updateMenuForm(LangID, MenuID, PageName, FormName, FormLink, RoleID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE dbo.Menu set PageName=?,FormName = ?,FormLink=?,RoleID=? WHERE MenuID = ? and LanguageID = ?', (PageName, FormName,
                                                         FormLink, RoleID, 
                                                         MenuID, LangID))
    except:
        return False
    conn.commit()
    return True


def CheckMenu(MenuID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dbo.SubMenu WHERE MenuID=?', MenuID)
    if cursor.fetchall():
        return True
    return False


def deleteMenu(LangID, MenuID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM dbo.Menu WHERE MenuID=? and LanguageID=?', (MenuID,
                                                                       LangID))
    except:
        return False
    conn.commit()
    return True


def getMenuID():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(MenuID) FROM dbo.Menu")
    top = cursor.fetchall()
    if not top[0][0]:
        return 0
    return top[0][0]


def updateSubMenuForm(LanguageID, MenuID, SubMenuID, FormName, FormLink,
                      RoleID):
    conn = getConnection()
    cursor = conn.cursor()
    # try:
    cursor.execute('UPDATE dbo.SubMenu set FormName = ?,FormLink=?,RoleID=? WHERE MenuID = ? and SubMenuID = ? and LanguageID = ?',
                   (FormName, FormLink, RoleID, MenuID, SubMenuID, LanguageID))
    # except:
    #     return False
    conn.commit()
    return True


def getSubMenuID(MenuID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(SubMenuID) FROM dbo.SubMenu WHERE MenuID = ?", (MenuID))
    top = cursor.fetchall()
    if not top[0][0]:
        return 0
    return top[0][0]


def NoMenu(MenuID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.Menu WHERE MenuID=? ', (MenuID))
    if cursor.fetchall() == []:
        return True
    return False


def deleteSubMenu(LangID, MenuID, SubMenuID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM dbo.SubMenu WHERE MenuID=? and LanguageID=? and SubMenuID=?', (MenuID, LangID, SubMenuID))
    except:
        return False
    conn.commit()
    return True


def deleteReg(LoginID):
    conn_log = getConnection()
    cursor = conn_log.cursor()

    cursor.execute(
        'DELETE FROM dbo.Login WHERE LoginID=?', LoginID)

    conn_reg = getConnection()
    cursor = conn_reg.cursor()
    cursor.execute(
        'DELETE FROM dbo.Registration WHERE LoginID=?', LoginID)
    conn_log.commit()
    conn_reg.commit()
    conn_log.close()
    conn_reg.close()
    return True


def IdeaReg(LoginID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.Idea WHERE LoginID = ?', LoginID)
    if cursor.fetchall():
        return True
    return False


def checkIdeaentry(IdeaID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.Media WHERE IdeaID = ?', IdeaID)
    if cursor.fetchall():
        return True
    cursor.execute(
        'SELECT * FROM dbo.IdeaCatSubCat WHERE IdeaID = ?', IdeaID)
    if cursor.fetchall():
        return True
    return False


def deleteIdea(IdeaID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM dbo.Idea WHERE IdeaID = ?', IdeaID)
    except:
        return False
    conn.commit()
    conn.close()
    return True


def updateICS(prev_IdeaID, prev_CatID, prev_SubCatID, new_IdeaID, new_CatID, new_SubCatID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE dbo.IdeaCatSubCat set IdeaID=?,CategoryID=?,SubCategoryID=? WHERE IdeaID=? and CategoryID=? and SubCategoryID=?', (new_IdeaID, new_CatID, new_SubCatID, prev_IdeaID,
                      prev_CatID, prev_SubCatID))
    except:
        return False
    conn.commit()
    conn.close()
    return True


def deleteICS(IdeaID, CategoryID, SubCategoryID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM dbo.IdeaCatSubCat WHERE IdeaID=? and CategoryID=? and SubCategoryID=?',
                       (IdeaID, CategoryID, SubCategoryID))
    except:
        return False
    conn.commit()
    conn.close()
    return True


def NoLogin(LoginID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dbo.Registration WHERE LoginID=?', LoginID)
    if cursor.fetchall():
        return True
    return False


def updateLogin(LoginID, Username, Password, RoleID, RoleName):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE dbo.Login set Username=?,Password=? WHERE LoginID=?',
            (Username, Password, LoginID))
    except:
        return False
    conn.commit()
    conn.close()
    return True


def deleteLogin(LoginID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM dbo.Login WHERE LoginID=?', LoginID)
    except:
        return False
    conn.commit()
    conn.close()
    return True


def LoginID():
    # Returns the maximum LoginID,the latest one!
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(LoginID) FROM dbo.Login")
    top = cursor.fetchall()
    if not top[0][0]:
        return 0
    return top[0][0]


def createLogin(LoginID, Username, Password, RoleID, RoleName, cr_by, cr_date):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO dbo.Login VALUES (?,?,?,?,?,?,?)',
                   (LoginID, Username, Password, RoleID, RoleName, cr_by, cr_date))
    conn.commit()
    return True


def updateLabelSA(LabelID, LanguageID, RoleID, PageName, LabelType, LabelValue):
    # SA - Superadmin
    conn = getConnection()
    cursor = conn.cursor()
    # try:
    print LabelID
    cursor.execute('UPDATE dbo.Label set RoleID=?,PageName=?,LabelType=?,LabelValue=? WHERE LabelID=? and LanguageID=?', (RoleID,
                                              PageName, LabelType, LabelValue,int(LabelID), int(LanguageID)))
    # except:
    #     return False
    conn.commit()
    conn.close()
    return True


def getLabelID():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(LabelID) FROM dbo.Label")
    top = cursor.fetchall()
    if not top[0][0]:
        return 0
    return top[0][0]


def deleteLabel(LabelID, LangID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM dbo.Label WHERE LabelID = ? and LanguageID=?',
            (LabelID, LangID))
    except:
        return False
    conn.commit()
    conn.close()
    return True


def getLangIDs():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.Language")
    langs = cursor.fetchall()
    LangIDs = []
    for data in langs:
        LangIDs.append(data[0])
    return LangIDs


def change_password(old_password,new_password,confirm_password,LoginID):
    conn = getConnection()
    cursor = conn.cursor()
    print cursor
    cursor.execute("SELECT Password FROM dbo.Login WHERE LoginID = ?",(LoginID))
    password = cursor.fetchall()[0][0]
    print password
    if new_password != confirm_password:
        return 2
    elif old_password != password:
        return 0
    else:
        cursor.execute("UPDATE dbo.Login SET Password = ? WHERE LoginID = ?",(new_password, LoginID))
        conn.commit()
    return True


def getContactID():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(ContactID) FROM dbo.Contact")
    top = cursor.fetchall()
    if not top[0][0]:
        return 0
    return top[0][0]


def insertEnquiry(Name, EmailID, Phone, Message):
    conn = getConnection()
    cursor = conn.cursor()
    ContactID = getContactID()
    try:
        cursor.execute(
                'INSERT INTO dbo.Contact VALUES (?, ?, ?, ?, ?)', (ContactID, Name, EmailID, Phone, Message))
        conn.commit()
    except:
        return False
    return True


def LoginDistrict():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT LoginID,DistrictID FROM dbo.Registration')
    return cursor.fetchall()


def distinctDistricts():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT DistrictID,DistrictName FROM dbo.District')
    return cursor.fetchall()
