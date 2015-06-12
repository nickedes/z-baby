import os
import pymssql
from configparser import ConfigParser
from datetime import datetime


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
        cursor.executemany(
            'INSERT INTO dbo.IdeaCatSubCat VALUES (%d, %d, %d)', vals)
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


def insertCat(CategoryID, LanguageID, CategoryValue, CreatedBy):
    conn = getConnection()
    cursor = conn.cursor()
    CreateDate = datetime.now()
    try:
        cursor.execute(
            'INSERT INTO dbo.Category VALUES (%d, %d, %s, %s, %s)', (LanguageID, CategoryID, CategoryValue, CreatedBy, CreateDate))
    except:
        return False
    conn.commit()
    return True


def insertSubCat(CategoryID, SubCategoryID, LanguageID, SubValue, CreatedBy):
    conn = getConnection()
    cursor = conn.cursor()
    CreateDate = datetime.now()
    # SubCategory (LanguageID, CategoryID, SubCategoryID, SubCategoryValue, CreatedBy, CreateDate)
    try:
        cursor.execute(
            'INSERT INTO dbo.SubCategory VALUES (%d, %d, %d, %s, %s, %s)', (LanguageID, CategoryID, SubCategoryID, SubValue, CreatedBy, CreateDate))
    except:
        return False
    conn.commit()
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
    try:
        cursor.execute(
            'INSERT INTO dbo.Menu VALUES (%d, %d, %s, %s, %s, %d, %s, %s)', menuvalues)
    except:
        return False
    conn.commit()
    return True


def insertCountry(LanguageID, CountryID, CountryName, CreatedBy):
    conn = getConnection()
    cursor = conn.cursor()
    CreateDate = datetime.now()
    try:
        cursor.execute(
            'INSERT INTO dbo.Country VALUES (%d, %d, %s, %s, %s)', (LanguageID, CountryID, CountryName, CreatedBy, CreateDate))
    except:
        return False
    conn.commit()
    return True
    # State (LanguageID, CountryID, StateID, StateName, CreatedBy, CreateDate)


def insertState(LanguageID, CountryID, StateID, StateName, CreatedBy):
    conn = getConnection()
    cursor = conn.cursor()
    CreateDate = datetime.now()
    try:
        cursor.execute(
            'INSERT INTO dbo.State VALUES (%d, %d, %d, %s, %s, %s)', (LanguageID, CountryID, StateID, StateName, CreatedBy, CreateDate))
    except:
        return False
    conn.commit()
    return True


def insertSubMenu(submenuvalues):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO dbo.SubMenu VALUES (%d, %d, %d, %s, %s, %d, %s, %s)', submenuvalues)
    except:
        return False
    conn.commit()
    return True


def insertLabel(labelvalues):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO dbo.Label VALUES (%d, %d, %d, %s, %s, %s, %s, %s)', labelvalues)
    except:
        return False
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


def updateIdea(IdeaID, title, stage_id, benefit_id, description, resource, support, implement_time, reach):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE dbo.Idea set IdeaTitle=%s,StageID=%d,BenefitID=%d,Description=%s,ResourcesRequired=%s,Support=%s,ImplementTime=%d, Reach=%s WHERE IdeaID = %d', (title, stage_id, benefit_id, description, resource, support, implement_time, reach, IdeaID))
        conn.commit()
    except:
        return False
    conn.close()
    return True


def updateMedia(IdeaID, Mvalue, Mtype, cr_date):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE dbo.Media set MediaValue=%s,CreateDate=%s WHERE IdeaID = %d and MediaType = %s', (Mvalue, cr_date, IdeaID, Mtype))
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
            'UPDATE dbo.Label set LabelValue=%s WHERE LabelID = %d and LanguageID = %d', (LabelValue, LabelID, LanguageID))
        conn.commit()
    except:
        return False
    conn.close()
    return True


def updateIdeaCatSubCat(idea_id, category_id, subcategory_id):
    # Todo: Improve
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM dbo.IdeaCatSubCat WHERE IdeaID=%d', (idea_id))
    conn.commit()
    vals = []
    for subcategory in subcategory_id:
        vals.append((idea_id, category_id, subcategory))
    try:
        cursor.executemany(
            'INSERT INTO dbo.IdeaCatSubCat VALUES (%d, %d, %d)', vals)
        conn.commit()
    except:
        return False
    return True


def getIdeaUnderOperator(LoginID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dbo.Idea WHERE CreatedBy = %s', str(LoginID))
    return cursor.fetchall()


def updateCat(LangID, CategoryID, CategoryValue):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE dbo.Category set CategoryValue = %s WHERE CategoryID = %d and LanguageID = %d', (CategoryValue, CategoryID, LangID))
    except:
        return False
    conn.commit()
    return True


def updateSubCat(LangID, CategoryID, SubCategoryID, CategoryValue):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE dbo.SubCategory set SubCategoryValue = %s WHERE CategoryID = %d and SubCategoryID = %d and LanguageID = %d',
                       (CategoryValue, CategoryID, SubCategoryID, LangID))
    except:
        return False
    conn.commit()
    return True


def updateMenu(MenuID, FormName):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE dbo.Menu set FormName = %s WHERE MenuID = %d', (FormName, MenuID))
    except:
        return False
    conn.commit()
    return True


def updateSubMenu(MenuID, SubMenuID, MenuValue):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE dbo.SubMenu set FormName = %s WHERE MenuID = %d and SubMenuID = %d',
                       (MenuValue, MenuID, SubMenuID))
    except:
        return False
    conn.commit()
    return True


def updateCountry(LangID, CountryID, CountryName):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE dbo.Country set CountryName = %s WHERE CountryID = %d and LanguageID = %d', (CountryName, CountryID, LanguageID))
    except:
        return False
    conn.commit()
    return True


def updateState(LangID, CountryID, StateID, StateName):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE dbo.State set StateName = %s WHERE LanguageID = %d and CountryID = %d and StateID = %d',
                       (StateName, LangID, CountryID, StateID))
    except:
        return False
    conn.commit()
    return True


def updateDistrict(LangID, CountryID, StateID, DistrictID, DistrictName):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE dbo.District set DistrictName = %s WHERE LanguageID = %d and CountryID = %d and StateID = %d and DistrictID = %d',
                       (DistrictName, LangID, CountryID, StateID, DistrictID))
    except:
        return False
    conn.commit()
    return True


def updateBlock(LangID, CountryID, StateID, DistrictID, BlockID, DistrictName):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE dbo.Block set BlockName = %s WHERE LanguageID = %d and CountryID = %d and StateID = %d and DistrictID = %d and BlockID =%d',
                       (DistrictName, LangID, CountryID, StateID, DistrictID, BlockID))
    except:
        return False
    conn.commit()
    return True


def SupdateMedia(MediaID, IdeaID, value, Mtype):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE dbo.Media set IdeaID = %d, MediaValue = %s, MediaType = %s WHERE MediaID = %d',
                       (IdeaID, value, Mtype, MediaID))
    except:
        return False
    conn.commit()
    return True


def NoIdea(IdeaID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dbo.Idea WHERE IdeaID=%d', IdeaID)
    if cursor.fetchall() == []:
        return True
    return False


def deleteMedia(MediaID, IdeaID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM dbo.Media WHERE MediaID=%d and IdeaID=%d', (MediaID, IdeaID))
    except:
        return False
    conn.commit()
    return True


def CheckCountry(CountryID):
    # Check if there is a state for this Country.
    # If yes then NO DELETION!
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dbo.State WHERE CountryID=%d', CountryID)
    if cursor.fetchall():
        return True
    return False


def deleteCountry(LangID, CountryID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM dbo.Country WHERE CountryID=%d and LanguageID=%d', (CountryID, LangID))
    except:
        return False
    conn.commit()
    return True


def getCountryID(LangID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(CountryID) FROM dbo.Country WHERE LanguageID = %d", LangID)
    top = cursor.fetchall()
    if not top:
        return 0
    return top[0][0]


def getStateID(LangID, CountryID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(StateID) FROM dbo.State WHERE CountryID = %d and LanguageID = %d", (CountryID, LangID))
    top = cursor.fetchall()
    if not top:
        return 0
    return top[0][0]


def CheckState(StateID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dbo.District WHERE StateID=%d', StateID)
    if cursor.fetchall():
        return True
    return False


def deleteState(LangID, CountryID, StateID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM dbo.State WHERE CountryID=%d and LanguageID=%d and StateID=%d',
            (CountryID, LangID, StateID))
    except:
        return False
    conn.commit()
    return True


def CheckDistrict(DistrictID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dbo.Block WHERE DistrictID=%d', DistrictID)
    if cursor.fetchall():
        return True
    return False


def deleteDistrict(LangID, CountryID, StateID, DistrictID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM dbo.District WHERE CountryID=%d and LanguageID=%d and StateID=%d and DistrictID=%d',
            (CountryID, LangID, StateID, DistrictID))
    except:
        return False
    conn.commit()
    return True


def NoCountry(CountryID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dbo.Country WHERE CountryID=%d', CountryID)
    if cursor.fetchall() == []:
        return True
    return False


def NoState(StateID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dbo.State WHERE StateID=%d', StateID)
    if cursor.fetchall() == []:
        return True
    return False


def getDistrictID(LangID, CountryID, StateID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(DistrictID) FROM dbo.District WHERE LanguageID =%d and CountryID = %d and StateID = %d", (LangID, CountryID, StateID))
    top = cursor.fetchall()
    if not top:
        return 0
    return top[0][0]


def NoDistrict(DistrictID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.District WHERE DistrictID=%d', DistrictID)
    if cursor.fetchall() == []:
        return True
    return False


def insertDistrict(LanguageID, CountryID, StateID, DistrictID, DistrictName, CreatedBy):
    conn = getConnection()
    cursor = conn.cursor()
    CreateDate = datetime.now()
    try:
        cursor.execute(
            'INSERT INTO dbo.District VALUES (%d, %d, %d, %d, %s, %s, %s)', (LanguageID, CountryID, StateID, DistrictID, DistrictName, CreatedBy, CreateDate))
    except:
        return False
    conn.commit()
    return True


def deleteBlock(LangID, CountryID, StateID, DistrictID, BlockID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM dbo.Block WHERE CountryID=%d and LanguageID=%d and StateID=%d and DistrictID=%d and BlockID=%d',
            (CountryID, LangID, StateID, DistrictID, BlockID))
    except:
        return False
    conn.commit()
    return True


def getBlockID(LangID, CountryID, StateID, DistrictID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(BlockID) FROM dbo.Block WHERE LanguageID = %d and CountryID = %d and StateID = %d \
         and DistrictID = %d", (LangID, CountryID, StateID, DistrictID))
    top = cursor.fetchall()
    if not top:
        return 0
    return top[0][0]


def insertBlock(LanguageID, CountryID, StateID, DistrictID, BlockID, BlockName, CreatedBy):
    conn = getConnection()
    cursor = conn.cursor()
    CreateDate = datetime.now()
    try:
        cursor.execute(
            'INSERT INTO dbo.Block VALUES (%d, %d, %d, %d, %d, %s, %s, %s)', (LanguageID, CountryID, StateID, DistrictID, BlockID, BlockName, CreatedBy, CreateDate))
    except:
        return False
    conn.commit()
    return True


def getCatID(LangID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(CategoryID) FROM dbo.Category WHERE LanguageID = %d", LangID)
    top = cursor.fetchall()
    if not top:
        return 0
    return top[0][0]


def CheckCategory(CategoryID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.SubCategory WHERE CategoryID=%d', CategoryID)
    if cursor.fetchall():
        return True
    return False


def NoCategory(CategoryID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.Category WHERE CategoryID=%d', CategoryID)
    if cursor.fetchall() == []:
        return True
    return False


def getSubCatID(LangID, CategoryID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(SubCategoryID) FROM dbo.SubCategory WHERE LanguageID = %d and CategoryID = %d", (LangID, CategoryID))
    top = cursor.fetchall()
    if not top:
        return 0
    return top[0][0]


def deleteCategory(LangID, CategoryID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM dbo.Category WHERE CategoryID=%d and LanguageID=%d', (CategoryID, LangID))
    except:
        return False
    conn.commit()
    return True


def deleteSub(LangID, CatID, SubCatID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM dbo.SubCategory WHERE LanguageID=%d  and CategoryID=%d and SubCategoryID=%d',
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
            'UPDATE dbo.Stage set StageValue = %s WHERE StageID = %d and LanguageID = %d', (StageName, StageID, LangID))
    except:
        return False
    conn.commit()
    return True


def deleteStage(LangID, StageID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM dbo.Stage WHERE StageID=%d and LanguageID=%d', (StageID, LangID))
    except:
        return False
    conn.commit()
    return True


def getStageID(LangID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(StageID) FROM dbo.Stage WHERE LanguageID = %d", LangID)
    top = cursor.fetchall()
    if not top:
        return 0
    return top[0][0]


def insertStage(LanguageID, StageID, value, CreatedBy):
    conn = getConnection()
    cursor = conn.cursor()
    CreateDate = datetime.now()
    try:
        cursor.execute(
            'INSERT INTO dbo.Stage VALUES (%d, %d, %s, %s, %s)', (LanguageID, StageID, value, CreatedBy, CreateDate))
    except:
        return False
    conn.commit()
    return True


def getLangID():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(LanguageID) FROM dbo.Language ")
    top = cursor.fetchall()
    if not top:
        return 0
    return top[0][0]


def insertLang(LanguageID, name, CreatedBy):
    conn = getConnection()
    cursor = conn.cursor()
    CreateDate = datetime.now()
    try:
        cursor.execute(
            'INSERT INTO dbo.Language VALUES (%d, %s, %s, %s)', (LanguageID, name, CreatedBy, CreateDate))
    except:
        return False
    conn.commit()
    return True
