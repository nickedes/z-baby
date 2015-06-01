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
    if 'username' in session:
        return redirect(url_for('home'))
    if 'LanguageID' not in session:
        session['LanguageID'] = 1
    if 'RoleID' not in session:
        session['RoleID'] = 1
    if 'userid' not in session:
        session['userid'] = 0
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
    submenuval = {submenu[2]: [submenu[1], submenu[3], submenu[4]]
                  for submenu in submenus
                  if submenu[0] == session['LanguageID']
                  and submenu[5] == session['RoleID']}
    return render_template('slash.html', label=labelval, menu=menuval,
                           submenu=submenuval,
                           userval=checkloggedin(session['userid']))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('signin.html', label=labelval, menu=menuval,
                               submenu=submenuval)
    else:
        username = request.form['username']
        logged_in_val = values.checkLogin(
            request.form['username'], request.form['password'])
        print(logged_in_val)
        if logged_in_val is None:
            return redirect(url_for('index'))
        else:
            session['RoleID'] = logged_in_val[0][0]
            session['username'] = username
            session['userid'] = logged_in_val[0][1]
            return redirect(url_for('home'))


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


@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        inno = values.checkInnovation(session['userid'])
        return render_template('home.html', label=labelval, menu=menuval,
                               submenu=submenuval,
                               userval=checkloggedin(session['userid']),
                               inno=inno)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.pop('userid', None)
    return redirect(url_for('index'))


@app.route('/register')
def register():
    country, state, district, block = values.levels()
    countrylist = {}
    for single_country in country:
        statelist = []
        for single_state in state:
            if single_state[1] == single_country[1]:
                statelist.append([single_state[3], single_state[2]])
        countrylist[single_country[1]] = statelist
    print(countrylist)
    statelist = {}
    for single_state in state:
        districtlist = []
        for single_district in district:
            if single_district[2] == single_state[2]:
                districtlist.append([single_district[4], single_district[3]])
        statelist[single_state[2]] = districtlist
    print(statelist)
    districtdict = {}
    for single_district in district:
        blocklist = []
        for single_block in block:
            if single_block[3] == single_district[3]:
                blocklist.append([single_block[5], single_block[4]])
        districtdict[single_district[3]] = blocklist
    print(districtdict)
    return render_template('register.html', label=labelval, menu=menuval,
                           submenu=submenuval, country=country, state=state,
                           district=district, block=block, clist=countrylist,
                           slist=statelist, dlist=districtdict)


@app.route('/update')
def update():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('update.html', label=labelval, menu=menuval,
                           submenu=submenuval,
                           userval=checkloggedin(session['userid']))


@app.route('/submit', methods=['GET','POST'])
def submit():
    if 'username' not in session:
        return redirect(url_for('index'))
    if request.method == 'GET':
        labellist = []
        for label in labels:
            if label[2].find('Idea') == 0:
                print (label)
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
                               userval=checkloggedin(session['userid']), labellist=labellist)
    if request.method == 'POST' and 'username' in session:
        # take in infinite data
        # put into DB
        #redirect user with success message
        pass
    return redirect(url_for('index'))



@app.route('/review')
def review():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('review.html', label=labelval, menu=menuval,
                           submenu=submenuval)


def checkloggedin(userid):
    if userid != 0:
        return True
    return False

if __name__ == '__main__':
    labels, menus, submenus, categories, subcategories = values.getValues()
    app.run(debug=True, host='0.0.0.0', port=3000)
