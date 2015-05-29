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
labelval = {}
menuval = {}
submenuval = {}


@app.route('/')
def index():
    global labelval
    global menuval
    global submenuval
    if 'LanguageID' not in session:
        session['LanguageID'] = 1
    if 'RoleID' not in session:
        session['RoleID'] = 1
    # play with variables

    labelval = {label[2]: label[3]
                for label in labels if label[1] == session['LanguageID']}
    for menu in menus:
        if menu[0] == session['LanguageID'] and menu[4] == session['RoleID']:
            flag = 1
            for submenu in submenus:
                if submenu[0] == session['LanguageID'] and submenu[5] == session['RoleID']:
                    if submenu[1] == menu[1]:
                        menuval[menu[1]] = [menu[2], menu[3], 1]
                        flag = 0
                        break
            if flag == 1:
                menuval[menu[1]] = [menu[2], menu[3], 0]

    submenuval = {submenu[1]: [submenu[4], submenu[5]] for submenu in submenus
                  if submenu[0] == session['LanguageID']
                  and submenu[5] == session['RoleID']}

    return render_template('slash.html', label=labelval, menu=menuval,
                           submenu=submenuval)


@app.route('/login')
def login():
    return render_template('signin.html', label=labelval, menu=menuval,
                           submenu=submenuval)


@app.route('/register')
def register():
    print(labelval, menuval, submenuval)
    return render_template('register.html', label=labelval, menu=menuval,
                           submenu=submenuval)

if __name__ == '__main__':
    labels, menus, submenus, categories, subcategories = values.getValues()
    app.run(debug=True, host='0.0.0.0', port=3000)
