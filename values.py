import os
import pyodbc
import ConfigParser
from datetime import datetime


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
    # try:
    cursor.execute(
        'INSERT INTO dbo.Label VALUES (%d, %d, %d, %s, %s, %s, %s, %s)', labelvalues)
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


def updateMenu(LangID, MenuID, FormName):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE dbo.Menu set FormName = %s WHERE MenuID = %d and LanguageID = %d', (FormName, MenuID, LangID))
    except:
        return False
    conn.commit()
    return True


def updateSubMenu(LanguageID, MenuID, SubMenuID, MenuValue):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE dbo.SubMenu set FormName = %s WHERE MenuID = %d and SubMenuID = %d and LanguageID = %d',
                       (MenuValue, MenuID, SubMenuID, LanguageID))
    except:
        return False
    conn.commit()
    return True


def updateCountry(LangID, CountryID, CountryName):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE dbo.Country set CountryName = %s WHERE CountryID = %d and LanguageID = %d', (CountryName, CountryID, LangID))
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
    if not top[0][0]:
        return 0
    return top[0][0]


def getStateID(LangID, CountryID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(StateID) FROM dbo.State WHERE CountryID = %d and LanguageID = %d", (CountryID, LangID))
    top = cursor.fetchall()
    if not top[0][0]:
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
    if not top[0][0]:
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
    if not top[0][0]:
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
    if not top[0][0]:
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
    if not top[0][0]:
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
    if not top[0][0]:
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
        'INSERT INTO dbo.Language VALUES (%s, %d, %s, %s)', (name, 0, CreatedBy, CreateDate))
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
        'INSERT INTO dbo.Label VALUES (%d, %d, %d, %s, %s, %s, %s, %s)', finallabel)
    conn.commit()
    cursor.executemany(
        'INSERT INTO dbo.Menu VALUES (%d, %d, %s, %s, %s, %d, %s, %s)', finalmenu)
    conn.commit()
    cursor.executemany(
        'INSERT INTO dbo.SubMenu VALUES (%d, %d, %d, %s, %s, %d, %s, %s)', finalsubmenu)
    conn.commit()
    cursor.executemany(
        'INSERT INTO dbo.Country VALUES (%d, %d, %s, %s, %s)', finalcountry)
    conn.commit()
    cursor.executemany(
        'INSERT INTO dbo.State VALUES (%d, %d, %d, %s, %s, %s)', finalstate)
    conn.commit()
    cursor.executemany(
        'INSERT INTO dbo.District VALUES (%d, %d, %d, %d, %s, %s, %s)', finaldistrict)
    conn.commit()
    cursor.executemany(
        'INSERT INTO dbo.Block VALUES (%d, %d, %d, %d, %d, %s, %s, %s)', finalblock)
    conn.commit()
    cursor.executemany(
        'INSERT INTO dbo.Benefit VALUES (%d, %d, %s, %s, %s)', finalbenefit)
    conn.commit()
    cursor.executemany(
        'INSERT INTO dbo.Stage VALUES (%d, %d, %s, %s, %s)', finalstage)
    conn.commit()
    cursor.executemany(
        'INSERT INTO dbo.Category VALUES (%d, %d, %s, %s, %s)', finalcategory)
    conn.commit()
    cursor.executemany(
        'INSERT INTO dbo.SubCategory VALUES (%d, %d, %d, %s, %s, %s)', finalsubcategory)
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
            'UPDATE dbo.Language set LanguageName = %s,MasterLanguage=%d WHERE LanguageID = %d', (name, masterlang, LangID))
    except:
        return False
    conn.commit()
    return True


def checkLang(LangID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dbo.Menu WHERE LanguageID=%d', LangID)
    if cursor.fetchall():
        return True
    cursor.execute('SELECT * FROM dbo.Benefit WHERE LanguageID=%d', LangID)
    if cursor.fetchall():
        return True
    cursor.execute('SELECT * FROM dbo.Stage WHERE LanguageID=%d', LangID)
    if cursor.fetchall():
        return True
    cursor.execute('SELECT * FROM dbo.Category WHERE LanguageID=%d', LangID)
    if cursor.fetchall():
        return True
    cursor.execute('SELECT * FROM dbo.Country WHERE LanguageID=%d', LangID)
    if cursor.fetchall():
        return True
    cursor.execute('SELECT * FROM dbo.Label WHERE LanguageID=%d', LangID)
    if cursor.fetchall():
        return True
    return False


def deleteLang(LangID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM dbo.Language WHERE LanguageID=%d', LangID)
    except:
        return False
    conn.commit()
    return True


def updateBenefit(LangID, BenefitID, value):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE dbo.Benefit set BenefitValue = %s WHERE BenefitID = %d and LanguageID = %d', (value, BenefitID, LangID))
    except:
        return False
    conn.commit()
    return True


def deleteBenefit(LangID, BenefitID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM dbo.Benefit WHERE BenefitID=%d and LanguageID=%d', (BenefitID, LangID))
    except:
        return False
    conn.commit()
    return True


def getBenefitID(LangID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(BenefitID) FROM dbo.Benefit WHERE LanguageID = %d", LangID)
    top = cursor.fetchall()
    if not top[0][0]:
        return 0
    return top[0][0]


def insertBenefit(LanguageID, BenefitID, value, CreatedBy):
    conn = getConnection()
    cursor = conn.cursor()
    CreateDate = datetime.now()
    try:
        cursor.execute(
            'INSERT INTO dbo.Benefit VALUES (%d, %d, %s, %s, %s)', (LanguageID, BenefitID, value, CreatedBy, CreateDate))
    except:
        return False
    conn.commit()
    return True


def updateMenuForm(LangID, MenuID, PageName, FormName, FormLink, RoleID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE dbo.Menu set PageName=%s,FormName = %s,FormLink=%s,RoleID\
            =%d WHERE MenuID = %d and LanguageID = %d', (PageName, FormName,
                                                         FormLink, RoleID, 
                                                         MenuID, LangID))
    except:
        return False
    conn.commit()
    return True


def CheckMenu(MenuID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dbo.SubMenu WHERE MenuID=%d', MenuID)
    if cursor.fetchall():
        return True
    return False


def deleteMenu(LangID, MenuID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM dbo.Menu WHERE MenuID=%d and LanguageID=%d', (MenuID,
                                                                       LangID))
    except:
        return False
    conn.commit()
    return True


def getMenuID(LangID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(MenuID) FROM dbo.Menu WHERE LanguageID = %d", LangID)
    top = cursor.fetchall()
    if not top[0][0]:
        return 0
    return top[0][0]


def updateSubMenuForm(LanguageID, MenuID, SubMenuID, FormName, FormLink,
                      RoleID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE dbo.SubMenu set FormName = %s,FormLink=%s,Role\
            ID=%s WHERE MenuID = %d and SubMenuID = %d and LanguageID = %d',
                       (FormName, FormLink, RoleID, MenuID, SubMenuID,
                        LanguageID))
    except:
        return False
    conn.commit()
    return True


def getSubMenuID(LangID, MenuID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(SubMenuID) FROM dbo.SubMenu WHERE LanguageID = %d and Men\
        uID = %d", (LangID, MenuID))
    top = cursor.fetchall()
    if not top[0][0]:
        return 0
    return top[0][0]


def NoMenu(LangID, MenuID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.Menu WHERE MenuID=%d and LanguageID=%d', (MenuID,
                                                                     LangID))
    if cursor.fetchall() == []:
        return True
    return False


def deleteSubMenu(LangID, MenuID, SubMenuID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM dbo.SubMenu WHERE MenuID=%d and LanguageID=%d and Su\
            bMenuID=%d', (MenuID, LangID, SubMenuID))
    except:
        return False
    conn.commit()
    return True


def deleteReg(LoginID):
    conn_log = getConnection()
    cursor = conn_log.cursor()

    cursor.execute(
        'DELETE FROM dbo.Login WHERE LoginID=%d', LoginID)

    conn_reg = getConnection()
    cursor = conn_reg.cursor()
    cursor.execute(
        'DELETE FROM dbo.Registration WHERE LoginID=%d', LoginID)
    conn_log.commit()
    conn_reg.commit()
    conn_log.close()
    conn_reg.close()
    return True


def IdeaReg(LoginID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.Idea WHERE LoginID = %d', LoginID)
    if cursor.fetchall():
        return True
    return False


def checkIdeaentry(IdeaID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM dbo.Media WHERE IdeaID = %d', IdeaID)
    if cursor.fetchall():
        return True
    cursor.execute(
        'SELECT * FROM dbo.IdeaCatSubCat WHERE IdeaID = %d', IdeaID)
    if cursor.fetchall():
        return True
    return False


def deleteIdea(IdeaID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM dbo.Idea WHERE IdeaID = %d', IdeaID)
    except:
        return False
    conn.commit()
    conn.close()
    return True


def updateICS(prev_IdeaID, prev_CatID, prev_SubCatID, new_IdeaID, new_CatID, new_SubCatID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE dbo.IdeaCatSubCat set IdeaID=%d,CategoryID=%d,\
            SubCategoryID=%d WHERE IdeaID=%d and CategoryID=%d and SubCategor\
            yID=%d', (new_IdeaID, new_CatID, new_SubCatID, prev_IdeaID,
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
        cursor.execute('DELETE FROM dbo.IdeaCatSubCat WHERE IdeaID=%d and Cat\
            egoryID=%d and SubCategoryID=%d',
                       (IdeaID, CategoryID, SubCategoryID))
    except:
        return False
    conn.commit()
    conn.close()
    return True


def NoLogin(LoginID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dbo.Registration WHERE LoginID=%d', LoginID)
    if cursor.fetchall():
        return True
    return False


def updateLogin(LoginID, Username, Password, RoleID, RoleName):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE dbo.Login set Username=%s,Password=%s WHERE LoginID=%d',
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
        cursor.execute('DELETE FROM dbo.Login WHERE LoginID=%d', LoginID)
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
    cursor.execute('INSERT INTO dbo.Login VALUES (%d,%s,%s,%d,%s,%s,%s)',
                   (LoginID, Username, Password, RoleID, RoleName, cr_by, cr_date))
    conn.commit()
    return True


def updateLabelSA(LabelID, LanguageID, RoleID, PageName, LabelType, LabelValue):
    # SA - Superadmin
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE dbo.Label set LanguageID=%d,RoleID=%d,PageName\
            =%s,LabelType=%s,LabelValue=%s', (LabelID, LanguageID, RoleID,
                                              PageName, LabelType, LabelValue))
    except:
        return False
    conn.commit()
    conn.close()
    return True


def getLabelID(LanguageID):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT max(LabelID) FROM dbo.Label WHERE LanguageID = %d", LanguageID)
    top = cursor.fetchall()
    if not top[0][0]:
        return 0
    return top[0][0]


def deleteLabel(LabelID, LangID):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM dbo.Label WHERE LabelID = %d and LanguageID=%d',
            (LabelID, LangID))
    except:
        return False
    conn.commit()
    conn.close()
    return True
