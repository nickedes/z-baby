import os
import datetime
import pymssql
from configparser import ConfigParser

def retrieveValues(lang=1):
	CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

	config = ConfigParser()
	config.read(os.path.join(CURRENT_DIR, 'config.ini'))

	server = config["Database"]["server"]
	user = config["Database"]["user"]
	password = config["Database"]["password"]
	conn = pymssql.connect(server, user, password, "ziiei")
	cursor = conn.cursor()
	cursor.execute('SELECT LabelType, LabelValue FROM dbo.Label where LanguageID=%d' %lang)
	labels = cursor.fetchall()
	cursor.execute('SELECT MenuID, FormName, FormLink FROM dbo.Menu where LanguageID=%d ORDER BY MenuID' %lang)
	menu = cursor.fetchall()
	cursor.execute('SELECT MenuID, FormName, FormLink FROM dbo.SubMenu where LanguageID=%d ORDER BY SubMenuID' %lang)
	submenu = cursor.fetchall()
	conn.close()
	menulist = []
	for menuitem in menu:
		menulist.append(0)
	for submenuitem in submenu:
		menulist[submenuitem[0]-1] = 1

	return { label[0]:label[1] for label in labels }, menu, submenu, menulist
