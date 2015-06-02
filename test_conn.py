import os
import datetime
import pymssql
from configparser import ConfigParser
from datetime import datetime

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

config = ConfigParser()
config.read(os.path.join(CURRENT_DIR, 'config.ini'))

server = config["Database"]["server"]
user = config["Database"]["user"]
password = config["Database"]["password"]

conn = pymssql.connect(server, user, password, "ziiei")
cursor = conn.cursor()
'''
<li><a href="/workflow">Workflow with timelines</a></li>
                    <li><a href="/apply">How to apply</a></li>
                    <li><a href="/benefits">Benefits</a></li>
                    <li><a href="/exmaples">Examples</a></li>
                    <li><a href="/terms">Terms and conditions</a></li>
                    '''
'''
cursor.executemany(
    "INSERT INTO dbo.SubMenu VALUES (%d, %d, %d, %s, %s, %d, %s, %s)",
    [(1, 5, 1, 'Workflow With Timelines', '/workflow', 1, 'admin', str(datetime.datetime.now())), 
    (1, 5, 2, 'How To Apply', '/apply', 1, 'admin', str(datetime.datetime.now())), 
    (1, 5, 3, 'Benefits', '/benefits', 1, 'admin', str(datetime.datetime.now())), 
    (1, 5, 4, 'Examples', '/examples', 1, 'admin', str(datetime.datetime.now())), 
    (1, 5, 5, 'Terms and Conditions', '/terms', 1, 'admin', str(datetime.datetime.now()))
    ])
,

cursor.execute(
    "INSERT INTO dbo.Login VALUES (%s, %s, %d, %s, %s, %s)",
    ('kwikadi', 'nkmittal', 1, 'user', 'admin', str(datetime.datetime.now())))

conn.commit()


cursor.executemany(
    "INSERT INTO dbo.Label VALUES (%d, %d, %s, %s, %s, %s)",
    [
        (24, 1, 'SigninUsername', 'Username', 'admin', str(datetime.now())),
        (25, 1, 'SigninPassword', 'Password', ' admin', str(datetime.now())),
        (26, 1, 'SigninLabel', 'Please Sign In', 'admin', str(datetime.now())),
        (27, 1, 'SigninButton', 'Sign In', 'admin', str(datetime.now()))
    ])




cursor.executemany(
    "INSERT INTO dbo.Label VALUES (%d, %d, %s, %s, %s, %s)",
    [
    (4, 1, 'RegistrationSchoolName', 'SchoolName', 'admin', str(datetime.datetime.now())),
    (5, 1, 'RegistrationSchoolAddress', 'SchoolAddress', 'admin', str(datetime.datetime.now())),
    (6, 1, 'RegistrationPhoneNumber', 'PhoneNumber', 'admin', str(datetime.datetime.now())),
    (7, 1, 'RegistrationDateOfJoining', 'DateOfJoining', 'admin', str(datetime.datetime.now())),
    (8, 1, 'RegistrationAwards', 'Awards', 'admin', str(datetime.datetime.now())),
    (9, 1, 'RegistrationEmployeeID', 'EmployeeID', 'admin', str(datetime.datetime.now())),
    (10, 1, 'RegistrationQualification', 'Qualification', 'admin', str(datetime.datetime.now())),
    (11, 1, 'RegistrationGender',  'Gender', 'admin', str(datetime.datetime.now())),
    (12, 1, 'RegistrationResidentialAddress', 'ResidentialAddress', 'admin', str(datetime.datetime.now())),
    (13, 1, 'RegistrationEmailID', 'EmailID', 'admin', str(datetime.datetime.now())),
    (14, 1, 'RegistrationDesignation', 'Designation', 'admin', str(datetime.datetime.now())),
    (15, 1, 'RegistrationBlockID', 'BlockID', 'admin', str(datetime.datetime.now())),
    (16, 1, 'RegistrationDistrictID', 'DistrictID', 'admin', str(datetime.datetime.now())),
    (17, 1, 'RegistrationStateID','StateID', 'admin', str(datetime.datetime.now())),
    (18, 1, 'RegistrationCountryID', 'CountryID', 'admin', str(datetime.datetime.now())),
    (19, 1, 'GenderMale', 'Male', 'admin', str(datetime.datetime.now())),
    (20, 1, 'GenderFemale', 'Female', 'admin', str(datetime.datetime.now())),
    (21, 1, 'RegistrationName', 'Name', 'admin', str(datetime.datetime.now()))
    ])

cursor.executemany(
    "INSERT INTO dbo.Label VALUES (%d, %d, %s, %s, %s, %s)",
    [
        (22, 1, 'Enquiry', 'Enquiry', 'admin', str(datetime.datetime.now())),
        (23, 1, 'Enquiry', 'Question', 'admin', str(datetime.datetime.now()))
    ])

conn.commit()
cursor.execute(
    "DELETE FROM dbo.Label where LabelType = 'Gender'"
    )
conn.commit()
'''

'''
cursor.executemany(
    "INSERT INTO dbo.Country VALUES (%d, %d, %s, %s, %s)",
    [(1, 1, 'India', 'admin', str(datetime.datetime.now()))]
)

cursor.executemany(
    "INSERT INTO dbo.State VALUES (%d, %d, %d, %s, %s, %s)",
    [
        (1, 1, 1, 'Uttar Pradesh', 'admin', str(datetime.datetime.now())),
        (1, 1, 2, 'Delhi', 'admin', str(datetime.datetime.now()))
    ]
)
conn.commit()

cursor.executemany(
    "INSERT INTO dbo.District VALUES (%d, %d, %d, %d, %s, %s, %s)",
    [
        (1, 1, 1, 1, 'Gz', 'admin', str(datetime.datetime.now())),
        (1, 1, 1, 2, 'Lk', 'admin', str(datetime.datetime.now()))
    ]
)
conn.commit()

cursor.executemany(
    "INSERT INTO dbo.Block VALUES (%d, %d, %d, %d, %d, %s, %s, %s)",
    [
        (1, 1, 1, 1, 1, 'A', 'admin', str(datetime.datetime.now())),
        (1, 1, 1, 1, 2, 'B', 'admin', str(datetime.datetime.now())),
        (1, 1, 1, 1, 3, 'C', 'admin', str(datetime.datetime.now())),
        (1, 1, 1, 2, 4, 'A', 'admin', str(datetime.datetime.now())),
        (1, 1, 1, 2, 5, 'A', 'admin', str(datetime.datetime.now())),
        (1, 1, 1, 2, 6, 'B', 'admin', str(datetime.datetime.now()))
    ]
)
conn.commit()


cursor.execute('SELECT * FROM dbo.Country')
row = cursor.fetchall()
print(row)


cursor.execute('SELECT * FROM dbo.State')
row = cursor.fetchall()
print(row)


cursor.execute('SELECT * FROM dbo.District')
row = cursor.fetchall()
print(row)


cursor.execute('SELECT * FROM dbo.Block')
row = cursor.fetchall()
print(row)

Idea (IdeaID, LoginID, IdeaTitle, StageID, BenefitID, CategoryID, 
    SubCategoryID, Description, ResourcesRequired, Support, ImplementTime, Reach, CreatedBy, CreateDate)


cursor.executemany(
    "INSERT INTO dbo.Label VALUES (%d, %d, %s, %s, %s, %s)",
    [
        (28, 1, 'IdeaTitle', '1. Title of your Idea:', 'admin', str(datetime.now())),
        (29, 1, 'IdeaStage', '2. What is the stage of your Zero-Investment Idea at the time of submitting this form? Select one option', ' admin', str(datetime.now())),
        (30, 1, 'IdeaBenefit', '3. What will be the top most benefit of implementing your idea? Select one option.', 'admin', str(datetime.now())),
        (31, 1, 'IdeaCategoryDropdown', '4. Your idea will be implemented in/for which of these areas? Please select one domain, and one or more corresponding sub-domains.', 'admin', str(datetime.now())),
        (32, 1, 'IdeaDescriptionLongtextbox', '5. Please describe your Zero-Investment Innovation Idea (in not more than 500 words).', 'admin', str(datetime.now())),
        (33, 1, 'IdeaMediaFileSelector', '6. If required, upload photographs showing how your idea can be implemented.', ' admin', str(datetime.now())),
        (34, 1, 'IdeaResourcesLongtextbox', '7. What resources are required to implement your idea?', 'admin', str(datetime.now())),
        (35, 1, 'IdeaSupportLongtextbox', '8. What support is required from the school administration to implement your idea?', 'admin', str(datetime.now())),
        (36, 1, 'IdeaImplementTime', '9. Approximately how many weeks will it take your school to implement your idea?', 'admin', str(datetime.now())),
        (37, 1, 'IdeaReach', '10. What will be the reach of the benefits of your idea?', ' admin', str(datetime.now())),
        (38, 1, 'IdeaExampleLongtextbox', '11. Can you provide some examples of the benefits of implementing your idea?', 'admin', str(datetime.now()))
    ])

cursor.executemany(
    "INSERT INTO dbo.Login VALUES (%s, %s, %d, %s, %s, %s)",
    [
        ('teacher', 'teacher', 1, 'teacher',
         'dummy', str(datetime.now())),
        ('dataentry', 'dataentry', 2, 'dataentry',
         'dummy', str(datetime.now())),
        ('viewer', 'viewer', 3, 'viewer', 'dummy', str(datetime.now())),
        ('admin', 'admin', 4, 'admin', 'dummy', str(datetime.now())),
        ('superadmin', 'superadmin', 5, 'superadmin',
         'dummy', str(datetime.now()))
    ])

conn.commit()

'''
cursor.execute('DELETE FROM dbo.Label WHERE LanguageID= 1')
conn.commit()
cursor.execute('SELECT * FROM dbo.Label WHERE LanguageID= 1')
row = cursor.fetchall()
print(row)
'''
cursor.execute('SELECT * FROM dbo.Label')
row = cursor.fetchall()
print(row)

cursor.execute('SELECT * FROM dbo.Login')
row = cursor.fetchall()
print(row)

cursor.execute('SELECT * FROM dbo.Menu')
row = cursor.fetchall()
print(row)

cursor.execute('SELECT * FROM dbo.SubMenu')
row = cursor.fetchall()
print(row)
# 
# cursor.execute('DELETE FROM dbo.Login where CreatedBy = %s' % "'" + "dummy" + "'")
'''
conn.commit()
conn.close()
