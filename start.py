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


def checkloggedin(userid):
    if userid != 0:
        return True
    return False


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    if 'LanguageID' not in session:
        session['LanguageID'] = 1
    if 'RoleID' not in session:
        session['RoleID'] = 0
    if 'userid' not in session:
        session['userid'] = 0
    # play with variables
    label_dict = {}
    for label in labels:
        if label[1] == session['LanguageID'] and label[2] == session['RoleID'] and label[3] == '/':
            label_dict[label[0]] = label[5]

    menubody = []
    for menu in menus:
        if menu[5] == session['RoleID'] and menu[0] == session['LanguageID'] and menu[2] == '/':
            menubody.append([menu[3], menu[4]])
    return render_template('slash.html', topmenu=topmenu, menubody=menubody, topsubmenu=topsubmenu, label=label_dict, menuarray=menuarray)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))
    if 'LanguageID' not in session:
        session['LanguageID'] = 1
    if 'RoleID' not in session:
        session['RoleID'] = 0
    if 'userid' not in session:
        session['userid'] = 0
    if 'username' in session:
        return redirect(url_for('index'))
    label_dict = {}
    if request.method == 'GET':
        for label in labels:
            if label[1] == session['LanguageID'] and label[2] == session['RoleID'] and label[3] == '/login':
                label_dict[label[0]] = label[5]
        return render_template('signin.html', topmenu=topmenu,
                               topsubmenu=topsubmenu,
                               menuarray=menuarray, label=label_dict)
    else:
        if 'signin' in request.form:
            username = request.form['username']
            logged_in_val = values.checkLogin(
                request.form['username'], request.form['password'])
            print(logged_in_val)
            if logged_in_val is None:
                return render_template('messages.html',
                                       userval=checkloggedin(
                                           session['userid']), menuarray=menuarray,
                                       topmenu=topmenu, topsubmenu=topsubmenu,
                                       message="Incorrect credentials, please try again!")

            else:
                session['RoleID'] = logged_in_val[0][0]
                session['username'] = username
                session['userid'] = logged_in_val[0][1]
                return redirect(url_for('home'))
        elif 'submit' in request.form:
            pass


@app.route('/home')
def home():
    if 'username' not in session:
        return render_template('messages.html',
            userval=checkloggedin(session['userid']),
            message="You are not logged in!")

    else:
        label_dict = {}
        for label in labels:
            if label[1] == session['LanguageID'] and label[2] == session['RoleID'] and label[3] == '/home':
                label_dict[label[0]] = label[5]
        print(label_dict)
        inno = values.checkInnovation(session['userid'])
        return render_template('home.html', topmenu=topmenu,
                               topsubmenu=topsubmenu,
                               menuarray=menuarray,
                               userval=checkloggedin(session['userid']),
                               inno=inno, label=label_dict)


@app.route('/about')
def about():
    return render_template('about.html', label=labelval, menu=menuval,
                           submenu=submenuval,
                           userval=checkloggedin(session['userid']))


@app.route('/workflow')
def workflow():
    return render_template('workflow.html', label=labelval, menu=menuval,
                           submenu=submenuval,
                           userval=checkloggedin(session['userid']))


@app.route('/howtoapply')
def howtoapply():
    return render_template('howtoapply.html', label=labelval, menu=menuval,
                           submenu=submenuval,
                           userval=checkloggedin(session['userid']))


@app.route('/benefits')
def benefits():
    return render_template('benefits.html', label=labelval, menu=menuval,
                           submenu=submenuval,
                           userval=checkloggedin(session['userid']))


@app.route('/examples')
def examples():
    return render_template('examples.html', label=labelval, menu=menuval,
                           submenu=submenuval,
                           userval=checkloggedin(session['userid']))


@app.route('/terms')
def terms():
    return render_template('terms.html', label=labelval, menu=menuval,
                           submenu=submenuval,
                           userval=checkloggedin(session['userid']))


@app.route('/faq')
def faq():
    return render_template('faq.html', label=labelval, menu=menuval,
                           submenu=submenuval,
                           userval=checkloggedin(session['userid']))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.pop('userid', None)
    return redirect(url_for('index'))


@app.route('/register')
def register():
    if 'username' in session:
        return redirect(url_for('index'))
    if 'LanguageID' not in session:
        session['LanguageID'] = 1
    if 'RoleID' not in session:
        session['RoleID'] = 0
    if 'userid' not in session:
        session['userid'] = 0
    if request.method == 'GET':
        country, state, district, block = values.levels()
        label_dict = {}
        for label in labels:
            if label[1] == session['LanguageID'] and label[2] == session['RoleID'] and label[3] == '/register':
                label_dict[label[0]] = [label[4], label[5]]

        countrylist = {}
        for single_country in country:
            statelist = []
            for single_state in state:
                if single_state[1] == single_country[1]:
                    statelist.append([single_state[3], single_state[2]])
            countrylist[single_country[1]] = statelist
        statelist = {}
        for single_state in state:
            districtlist = []
            for single_district in district:
                if single_district[2] == single_state[2]:
                    districtlist.append(
                        [single_district[4], single_district[3]])
            statelist[single_state[2]] = districtlist
        districtdict = {}
        for single_district in district:
            blocklist = []
            for single_block in block:
                if single_block[3] == single_district[3]:
                    blocklist.append([single_block[5], single_block[4]])
            districtdict[single_district[3]] = blocklist
        return render_template('register.html',topmenu=topmenu,
                               topsubmenu=topsubmenu,
                               menuarray=menuarray, country=country, state=state,
                               district=district, block=block, clist=countrylist,
                               slist=statelist, dlist=districtdict , label=label_dict)
    else:
        pass


@app.route('/update')
def update():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('update.html', label=labelval, menu=menuval,
                           submenu=submenuval,
                           userval=checkloggedin(session['userid']))


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if 'username' not in session:
        return render_template('messages.html', label=labelval, menu=menuval,
                               submenu=submenuval, userval=checkloggedin(
                                   session['userid']),
                               message="You are not logged in!")

    if request.method == 'GET':
        labellist = []
        for label in labels:
            if label[2].find('Idea') == 0:
                print(label)
                if label[2].find('Longtextbox') >= 0:
                    labellist.append([label[3], label[2], 'Longtextbox'])
                elif label[2].find('Dropdown') >= 0:
                    labellist.append([label[3], label[2], 'Dropdown'])
                elif label[2].find('FileSelector') >= 0:
                    labellist.append([label[3], label[2], 'FileSelector'])
                else:
                    labellist.append([label[3], label[2], 'Textbox'])
        return render_template('submit.html', label=labelval, menu=menuval,
                               submenu=submenuval,
                               userval=checkloggedin(session['userid']),
                               labellist=labellist)
    if request.method == 'POST' and 'username' in session:
        # take in infinite data
        # put into DB
        # redirect user with success message
        return render_template('messages.html', label=labelval, menu=menuval,
                               submenu=submenuval, userval=checkloggedin(
                                   session['userid']),
                               message="lolpol ho hi gaya")

    return redirect(url_for('index'))


@app.route('/review')
def review():
    if 'username' not in session:
        return render_template('messages.html', label=labelval, menu=menuval,
                               submenu=submenuval, userval=checkloggedin(
                                   session['userid']),
                               message="You are not logged in!")

    return render_template('review.html', label=labelval, menu=menuval,
                           submenu=submenuval)


if __name__ == '__main__':
    labels, menus, submenus, categories, subcategories = values.getValues()
    topmenu = []
    topsubmenu = []
    menuarray = [0 for menu in menus if menu[5] == -1]
    for menu in menus:
        if menu[5] == -1:
            topmenu.append([menu[3], menu[4], menu[1]])
        for submenu in submenus:
            if submenu[5] == -1 and submenu[1] == menu[1]:
                menuarray[submenu[1]-1] = 1
                topsubmenu.append([submenu[1], submenu[3], submenu[4]])
    app.run(debug=True, host='0.0.0.0', port=3000)
