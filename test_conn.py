import os
import datetime
import pymssql
from configparser import ConfigParser

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
cursor.execute('SELECT * FROM dbo.Login')
row = cursor.fetchall()
print(row)
conn.close()
