import os
from flask import (
    Flask,
    render_template,
    session,
    url_for,
    redirect,
    request
)

from errors import showerrors
import values


app = Flask(__name__)
app.secret_key = os.urandom(24)

showerrors(app)


@app.route('/')
def index():
    if 'LanguageID' not in session:
        session['LanguageID'] = 1
    if 'RoleID' not in session:
        session['RoleID'] = 1
    # play with variables
    labelval = {label[2]: label[3]
                for label in labels if label[1] == session['LanguageID']}
    menuval = {menu[1]: [menu[2], menu[3]]
               for menu in menus if menu[0] == session['LanguageID']
               and menu[4] == session['RoleID']}
    submenuval = {submenu[1]: [submenu[4], submenu[5]] for submenu in submenus
                  if submenu[0] == session['LanguageID']
                  and submenu[5] == session['RoleID']}
    return render_template('slash.html', label=labelval, menu=menuval,
                           submenu=submenuval)

if __name__ == '__main__':
    labels, menus, submenus, categories, subcategories = values.getValues(1)
    app.run(debug=True, host='0.0.0.0', port=3000)
