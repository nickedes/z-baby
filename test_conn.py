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


cursor.execute('DELETE FROM dbo.Label WHERE LanguageID= 1')
conn.commit()
cursor.execute('SELECT * FROM dbo.Label WHERE LanguageID= 1')
row = cursor.fetchall()
print(row)

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

Menu (LanguageID, MenuID, PageName, FormName, FormLink, RoleID, CreatedBy, CreateDate)

cursor.executemany('INSERT INTO dbo.Label values (%d, %d, %d, %s, %s, %s, %s, %s)',
    [1,1,0,'/',''])

cursor.executemany('INSERT INTO dbo.Menu values (%d, %d, %s, %s, %s, %d, %s, %s)',
    [(1,1,'/','Home','/', -1, 'nickedes', str(datetime.now())),
    (1,2,'/','About Us','#', -1, 'kwikadi', str(datetime.now())),
    (1,3,'/','ZIIEI','#', -1, 'nickedes', str(datetime.now())),
    (1,4,'/','FAQ','/faq', -1, 'kwikadi', str(datetime.now())),
    (1,5,'/','Contact Us','/contact', -1, 'nickedes', str(datetime.now())),
    (1,6,'/','Login','/login', 0, 'kwikadi', str(datetime.now())),
    (1,7,'/','Register','/register', 0, 'nickedes', str(datetime.now()))
    ])

SubMenu (LanguageID, MenuID, SubMenuID, FormName, FormLink, RoleID, CreatedBy, CreateDate)

cursor.executemany('INSERT INTO dbo.SubMenu values (%d, %d, %d, %s, %s, %d, %s, %s)',
    [(1,2,1,'ZIIEI', '/about/ziiei',-1, 'nickedes', str(datetime.now())),
    (1,2,2,'Sri Aurobindo Society','/about/sas', -1, 'kwikadi', str(datetime.now())),
    (1,2,3,'Litchi', '/about/litchi', -1,'nickedes', str(datetime.now())),
    (1,2,4,'U.P. Government','/about/upgovt', -1, 'kwikadi', str(datetime.now())),
    (1,3,1,'Workflow With Timelines','/ziiei/workflow', -1, 'nickedes', str(datetime.now())),
    (1,3,2,'How To Apply','/ziiei/apply', -1, 'kwikadi', str(datetime.now())),
    (1,3,3,'Benefits','/ziiei/benefits', -1, 'nickedes', str(datetime.now())),
    (1,3,4,'Examples','/ziiei/examples', -1, 'kwikadi', str(datetime.now())),
    (1,3,5,'Terms and Conditions','/ziiei/terms', -1, 'nickedes', str(datetime.now()))
    ])

Label (LabelID, LanguageID, RoleID, PageName, LabelType, LabelValue, CreatedBy, CreateDate)

cursor.executemany(
    "INSERT INTO dbo.Label values (%d, %d, %d, %s, %s, %s, %s, %s)",
    [
        (1, 1, 0, '/login', 'text', 'Please Sign In',
         'kwikadi', str(datetime.now())),
        (2, 1, 0, '/login', 'text', 'Username',
         'kwikadi', str(datetime.now())),
        (3, 1, 0, '/login', 'text', 'Password',
         'kwikadi', str(datetime.now())),
        (4, 1, 0, '/login', 'text', 'Sign In', 'kwikadi', str(datetime.now())),
        (5, 1, 0, '/login', 'text', 'Forgot Password',
         'kwikadi', str(datetime.now())),
        (6, 1, 0, '/login', 'text', 'Please enter a Username',
         'kwikadi', str(datetime.now())),
        (7, 1, 0, '/login', 'title', 'Sign In',
         'kwikadi', str(datetime.now())),
        (8, 1, 0, '/', 'title', 'Welcome to Ziiei',
         'kwikadi', str(datetime.now()))
    ]
)
conn.commit()


cursor.executemany(
    "INSERT INTO dbo.Label values (%d, %d, %d, %s, %s, %s, %s, %s)",
    [
        (9, 1, 0, '/home', 'title', 'ZIIEI',
         'kwikadi', str(datetime.now()))
    ])
conn.commit()
cursor.execute('UPDATE dbo.Label set LabelValue = %s  where LabelID = %d' % (
    "'ZIIEI-teacher'", 9))

conn.commit()

cursor.execute('UPDATE dbo.Label set RoleID = %d  where LabelID = %d' % (1, 9))

cursor.executemany(
    "INSERT INTO dbo.Label VALUES (%d, %d, %d, %s,%s, %s, %s, %s)",
    [
        (10, 1, 0, '/register', 'Textbox', 'Name', 'nickedes', str(datetime.now())),
        (11, 1, 0, '/register', 'Textbox', 'EmployeeID','nickedes', str(datetime.now())),
        (12, 1, 0, '/register', 'DateSelector', 'Date of Birth', 'nickedes', str(datetime.now())),
        (13, 1, 0, '/register', 'Textarea', 'Qualification', 'nickedes', str(datetime.now())),
        (14, 1, 0, '/register', 'Text','Gender', 'nickedes', str(datetime.now())),
        (15, 1, 0, '/register', 'RadioButton', 'Female', 'nickedes', str(datetime.now())),
        (16, 1, 0, '/register', 'RadioButton', 'Male', 'nickedes', str(datetime.now())),
        (17, 1, 0, '/register', 'DateSelector', 'DateOfJoining', 'nickedes', str(datetime.now())),
        (18, 1, 0, '/register', 'Textarea', 'Awards', 'nickedes', str(datetime.now())),
        (19, 1, 0, '/register', 'Textarea', 'ResidentialAddress', 'nickedes', str(datetime.now())),
        (20, 1, 0, '/register', 'Textbox', 'PhoneNumber', 'nickedes', str(datetime.now())),
        (21, 1, 0, '/register', 'Textbox', 'EmailID', 'nickedes', str(datetime.now())),
        (22, 1, 0, '/register', 'Textbox', 'SchoolName', 'nickedes', str(datetime.now())),
        (23, 1, 0, '/register', 'Textbox', 'Designation', 'nickedes', str(datetime.now())),
        (24, 1, 0, '/register', 'Textarea', 'Subjects', 'nickedes', str(datetime.now())),
        (25, 1, 0, '/register', 'Textarea', 'SchoolAddress', 'nickedes', str(datetime.now())),
        (26, 1, 0, '/register', 'Dropdown', 'CountryID', 'nickedes', str(datetime.now())),
        (27, 1, 0, '/register', 'Dropdown', 'StateID', 'nickedes', str(datetime.now())),
        (28, 1, 0, '/register', 'Dropdown', 'DistrictID', 'nickedes', str(datetime.now())),
        (29, 1, 0, '/register', 'Dropdown', 'BlockID', 'nickedes', str(datetime.now()))
    ])

conn.commit()

cursor.execute('UPDATE dbo.Label set LabelValue = %s  where LabelID = %d' % ("'Employee ID'", 11))
conn.commit()
cursor.execute('UPDATE dbo.Label set LabelValue = %s  where LabelID = %d' % ("'Date Of Joining'", 17))
conn.commit()
cursor.execute('UPDATE dbo.Label set LabelValue = %s  where LabelID = %d' % ("'Residential Address'", 19))
conn.commit()
cursor.execute('UPDATE dbo.Label set LabelValue = %s  where LabelID = %d' % ("'Phone Number'", 20))
conn.commit()
cursor.execute('UPDATE dbo.Label set LabelValue = %s  where LabelID = %d' % ("'Email ID'", 21))
conn.commit()
cursor.execute('UPDATE dbo.Label set LabelValue = %s  where LabelID = %d' % ("'School Name'", 22))
conn.commit()
cursor.execute('UPDATE dbo.Label set LabelValue = %s  where LabelID = %d' % ("'School Address'", 25))
conn.commit()
cursor.execute('UPDATE dbo.Label set LabelValue = %s  where LabelID = %d' % ("'Country'", 26))
conn.commit()
cursor.execute('UPDATE dbo.Label set LabelValue = %s  where LabelID = %d' % ("'State'", 27))
conn.commit()
cursor.execute('UPDATE dbo.Label set LabelValue = %s  where LabelID = %d' % ("'District'", 28))
conn.commit()
cursor.execute('UPDATE dbo.Label set LabelValue = %s  where LabelID = %d' % ("'Block'", 29))
conn.commit()

cursor.executemany(
    "INSERT INTO dbo.Label values (%d, %d, %d, %s, %s, %s, %s, %s)",
    [
        (30, 1, 0, '/register', 'text', 'Please enter your Registration details',
         'kwikadi', str(datetime.now()))
    ])
conn.commit()

Menu (LanguageID, MenuID, PageName, FormName, FormLink, RoleID, CreatedBy, CreateDate)

cursor.executemany('INSERT INTO dbo.Menu values (%d, %d, %s, %s, %s, %d, %s, %s)',
    [(1,8,'/home','Update Personal Information','/update', 1, 'nickedes', str(datetime.now())),
    (1,9,'/home','Submit Innovation','/submit', 1, 'kwikadi', str(datetime.now())),
    (1,10,'/home','Review Innovation','/review', 1, 'nickedes', str(datetime.now())),
    (1,11,'/home','Create Techer Profile','/create', 2, 'kwikadi', str(datetime.now())),
    (1,12,'/home','Submit Teacher Innovation','/submit', 2, 'nickedes', str(datetime.now())),
    (1,13,'/home','Update Teacher Profile','/update', 2, 'kwikadi', str(datetime.now())),
    (1,14,'/home','Review Teacher Innovation','/review', 2, 'nickedes', str(datetime.now())),
    (1,15,'/home','View Innovations','/view', 3, 'kwikadi', str(datetime.now())),
    (1,16,'/home','Edit Tables','/edit', 4, 'nickedes', str(datetime.now())),
    (1,17,'/home','Edit Tables','/edit', 5, 'kwikadi', str(datetime.now())),
    ])
Label (LabelID, LanguageID, RoleID, PageName, LabelType, LabelValue, CreatedBy, CreateDate)
cursor.executemany(
    "INSERT INTO dbo.Label VALUES (%d, %d, %d, %s, %s, %s, %s, %s)",
    [
        (31, 1, 1, '/submit', 'Textbox', 'Title of your Idea:','nickedes', str(datetime.now())),
        (32, 1, 1, '/submit', 'Text', "The title of your idea should convey the most important aspect, such as the issue solved through this idea, the key benefit of this idea, who will experience the benefit of this idea, etc.",'nickedes', str(datetime.now())),
        (33, 1, 1, '/submit', 'Dropdown', 'What is the stage of your Zero-Investment Idea at the time of submitting this form? Select one option','nickedes', str(datetime.now())),
        (34, 1, 1, '/submit', 'Dropdown', 'What will be the top most benefit of implementing your idea? Select one option.','nickedes', str(datetime.now())),
        (35, 1, 1, '/submit', 'Text', 'The outcomes listed here have been identified as the priority issues for transforming Education in your State. We are mainly looking for ideas that can lead to at least one of these outcomes.','nickedes', str(datetime.now())),
        (36, 1, 1, '/submit', 'Dropdown', 'Your idea will be implemented in/for which of these areas? Please select one domain, and one or more corresponding sub-domains.','nickedes', str(datetime.now())),
        (37, 1, 1, '/submit', 'Text', 'This refers is to the processes and procedures that your idea can improve. A detailed explanation is available here.','nickedes', str(datetime.now())),
        (38, 1, 1, '/submit', 'Textarea', 'Please describe your Zero-Investment Innovation Idea (in not more than 500 words).','nickedes', str(datetime.now())),
        (39, 1, 1, '/submit', 'Text', 'Please include details of how your idea can be implemented and how it works. You may choose to write it step-wise (Step 1, Step 2, etc.) or in bullet points. It is advisable to write the description on a separate document and when you are sure that you have provided all the important details, you can copy-paste it in this column.','nickedes', str(datetime.now())),
        (40, 1, 1, '/submit', 'Textbox', 'If required, upload photographs showing how your idea can be implemented.','nickedes', str(datetime.now())),
        (41, 1, 1, '/submit', 'Text', 'Although this is optional, it is advisable to upload photographs of your idea as it provides a better picture of the outcome. Examples of photographs are: students, teacher, etc. using your innovative teaching tool, image of a new admission form you have designed, parents and community participating in a school initiative, diagram of a new process you have created, how your school looked before and how it has improved after the implementation of your idea, or image of a classroom teaching technique you have designed. The photographs should be at least 200KB in size.','nickedes', str(datetime.now())),
        (42, 1, 1, '/submit', 'Textarea', 'What resources are required to implement your idea?','nickedes', str(datetime.now())),
        (43, 1, 1, '/submit', 'Textarea', 'Resources may include the number of students, painting material, stationery items, photocopies of documents, electricity connection, a new room in school building, etc.','nickedes', str(datetime.now())),
        (44, 1, 1, '/submit', 'Textarea', 'What support is required from the school administration to implement your idea?','nickedes', str(datetime.now())),
        (45, 1, 1, '/submit', 'Text', 'For instance, computer skills training for 1 teacher, a circular to be issued by the management, permission to take students on a field trip, etc.','nickedes', str(datetime.now())),
        (46, 1, 1, '/submit', 'Textbox', 'Approximately how many weeks will it take your school to implement your idea?','nickedes', str(datetime.now())),
        (47, 1, 1, '/submit', 'Textarea', 'What will be the reach of the benefits of your idea?','nickedes', str(datetime.now())),
        (48, 1, 1, '/submit', 'Textarea','Please specify who will be impacted and in what numbers. For instance, 75 students of your class, or parents of 75 children of your class and 30 teachers in your school.', 'nickedes', str(datetime.now())),
        (49, 1, 1, '/submit', 'Textarea','Can you provide some examples of the benefits of implementing your idea?', 'nickedes', str(datetime.now())),
        (50, 1, 1, '/submit', 'Textarea', "Please describe a particular incidence (or a hypothetical situation if your idea has not been implemented yet) to show in which was a student, or a teacher, or a school will be benefitted by your innovative idea. For instance, if you have modified the admission process, how will it help the school administration to maintain better records. Or, another example is, if you have devices a new teaching tool, how will a slow learner child use it for learning?",'nickedes',str(datetime.now()))
    ])

cursor.executemany(
    "INSERT INTO dbo.Label VALUES (%d, %d, %d, %s, %s, %s, %s, %s)",
    [
        (51, 1, 1, '/submit', 'head', 'Please enter the following details:','nickedes', str(datetime.now())),
        (52, 1, 1, '/submit', 'Text', "Submit",'nickedes', str(datetime.now()))
    ]);

'''
cursor.executemany(
    "INSERT INTO dbo.Benefit VALUES (%d, %d, %s, %s, %s)",
    [
        (1, 1,"Improvement in learning outcomes and reduction in learning gaps" ,'nickedes',str(datetime.now())),
        (1, 2,"Create more supportive environment for girl child education" ,'nickedes',str(datetime.now())),
        (1, 3,"Facilitate inclusive education for children with special needs" ,'nickedes',str(datetime.now())),
        (1, 4,"Create an enquiry-led self-learning environment in the classroom/school" ,'nickedes',str(datetime.now())),
        (1, 5,"Increase the involvement of students’ parents in Education" ,'nickedes',str(datetime.now())),
        (1, 6,"Improve the rate of student enrolment in schools " ,'nickedes',str(datetime.now())),
        (1, 7,"Reduce the rate of student drop-out from schools" ,'nickedes',str(datetime.now())),
        (1, 8,"Enhancement of deeper human values in the students, staff, school or community" ,'nickedes',str(datetime.now())),
        (1, 9,"Improve the motivation level of teachers towards their profession" ,'nickedes',str(datetime.now())),
        (1, 10,"None of these" ,'nickedes',str(datetime.now())),
    ])
conn.commit()
cursor.executemany(
    "INSERT INTO dbo.Stage VALUES (%d, %d, %s, %s, %s)",
    [
        (1,1,'It is currently being implemented in a school, but its benefits have not been mapped yet.' ,'nickedes',str(datetime.now())),
        (1,2,'Already implemented and your school is experiencing its benefits' ,'nickedes',str(datetime.now())),
        (1,3,'It is a concept which has not been implemented anywhere yet' ,'nickedes',str(datetime.now()))
    ])
conn.commit()
cursor.executemany(
    "INSERT INTO dbo.Category VALUES (%d, %d, %s, %s, %s)",
    [
        (1, 1, "Scholastic Processes",'nickedes',str(datetime.now())),
        (1, 2, "Co-scholastic Processes and Outcomes",'nickedes',str(datetime.now())),
        (1, 3, "Infrastructure",'nickedes',str(datetime.now())),
        (1, 4, "Education Stakeholders",'nickedes',str(datetime.now())),
        (1, 5, "Management & Administration",'nickedes',str(datetime.now())),
        (1, 6, "Leadership",'nickedes',str(datetime.now()))
    ])
    
conn.commit()
cursor.executemany(
    "INSERT INTO dbo.SubCategory VALUES (%d, %d, %d, %s, %s, %s)",
    [
        (1, 1, 1,"Curriculum Planning",'nickedes',str(datetime.now())),
        (1, 1, 2,"Teaching and Learning Process",'nickedes',str(datetime.now())),
        (1, 1, 3,"Student Performance Assessment",'nickedes',str(datetime.now())),
        (1, 2, 1,"Inculcating Life Skills",'nickedes',str(datetime.now())),
        (1, 2, 2,"Inculcating Values",'nickedes',str(datetime.now())),
        (1, 2, 3,"Improving Attitude towards Teaching / Learning",'nickedes',str(datetime.now())),
        (1, 2, 4,"Career counselling",'nickedes',str(datetime.now())),
        (1, 2, 5,"Visual and Performing Arts",'nickedes',str(datetime.now())),
        (1, 2, 6,"Extra-curricular activities",'nickedes',str(datetime.now())),
        (1, 2, 7,"Health and Physical Activities",'nickedes',str(datetime.now())),
        (1, 3, 1,"Classrooms, Library, Laboratory, Computer Labs.....etc.",'nickedes',str(datetime.now())),
        (1, 3, 2,"Principal's Office, Staff Room and Administration Offices",'nickedes',str(datetime.now())),
        (1, 3, 3,"Sports and Games Facilities, Hobby Rooms, Arts and Music Facilities.",'nickedes',str(datetime.now())),
        (1, 3, 4,"Girl's rest room, infirmary, water and sanitation, Health Management Facilities.",'nickedes',str(datetime.now())),
        (1, 3, 5,"Furniture, Lightening Sanitation",'nickedes',str(datetime.now())),
        (1, 3, 6,"Safety and Disaster Management provisions",'nickedes',str(datetime.now())),
        (1, 3, 7,"Provision for differently abled children and inclusive practices.",'nickedes',str(datetime.now())),
        (1, 3, 8,"Eco-Friendly Orientation, Aesthetics, Lawns and Green Plants",'nickedes',str(datetime.now())),
        (1, 4, 1,"Teaching staff",'nickedes',str(datetime.now())),
        (1, 4, 2,"Parents",'nickedes',str(datetime.now())),
        (1, 4, 3,"Alumni",'nickedes',str(datetime.now())),
        (1, 4, 4,"Students",'nickedes',str(datetime.now())),
        (1, 4, 5,"Administrative staff",'nickedes',str(datetime.now())),
        (1, 4, 6,"Alumni",'nickedes',str(datetime.now())),
        (1, 4, 7,"Community",'nickedes',str(datetime.now())),
        (1, 5, 1,"Institutional Planning",'nickedes',str(datetime.now())),
        (1, 5, 2,"Institutional Improvement and Process of Accreditation and Certification",'nickedes',str(datetime.now())),
        (1, 5, 3,"Goal Setting and Policy Making",'nickedes',str(datetime.now())),
        (1, 5, 4,"Effective Co-Ordination within the school",'nickedes',str(datetime.now())),
        (1, 5, 5,"Resource Management",'nickedes',str(datetime.now())),
        (1, 5, 6,"Relationship Management (staff, parents, community, alumni etc.)",'nickedes',str(datetime.now())),
        (1, 5, 7,"Data and Record Maintenance",'nickedes',str(datetime.now())),
        (1, 5, 8,"Oral and Written Communication",'nickedes',str(datetime.now())),
        (1, 5, 9,"Standard Operating Procedures ",'nickedes',str(datetime.now())),
        (1, 5, 10,"Financial Administration",'nickedes',str(datetime.now())),
        (1, 6, 1,"Vision and Mission Statement",'nickedes',str(datetime.now())),
        (1, 6, 2,"Strategic plans for the school improvement",'nickedes',str(datetime.now())),
        (1, 6, 3,"Quality and Change Management",'nickedes',str(datetime.now())),
        (1, 6, 4,"Scholastic Leadership",'nickedes',str(datetime.now())),
        (1, 6, 5,"Innovative practices",'nickedes',str(datetime.now()))
    ])
conn.commit()
cursor.execute('SELECT * from dbo.Stage')
row = cursor.fetchall()
print(row)
cursor.execute('SELECT * from dbo.Category')
row = cursor.fetchall()
print(row)
cursor.execute('SELECT * from dbo.SubCategory')
row = cursor.fetchall()
print(row)
cursor.execute('SELECT * from dbo.Benefit')
row = cursor.fetchall()
print(row)
conn.close()
