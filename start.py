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
        session['LanguageID'] = masterlang
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
        menulist = []
        for menu in menus:
            if menu[0] == session['LanguageID'] and menu[2] == '/home' and menu[5] == session['RoleID']:
                menulist.append([menu[3], menu[4]])
        inno = values.checkInnovation(session['userid'])
        return render_template('home.html', topmenu=topmenu,
                               topsubmenu=topsubmenu,
                               menuarray=menuarray,
                               userval=checkloggedin(session['userid']),
                               inno=inno, label=label_dict,
                               menulist=menulist)


@app.route('/about/<pagename>')
def about(pagename):
    if 'LanguageID' not in session:
        session['LanguageID'] = 1
    if 'RoleID' not in session:
        session['RoleID'] = 0
    if 'userid' not in session:
        session['userid'] = 0

    if pagename == 'ziiei':
        return render_template('ziiei.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray,
                               userval=checkloggedin(session['userid']))
    elif pagename == 'sas':
        return render_template('sas.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray,
                               userval=checkloggedin(session['userid']))
    elif pagename == 'litchi':
        return render_template('litchi.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray,
                               userval=checkloggedin(session['userid']))
    elif pagename == 'upgovt':
        return render_template('upgovt.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray,
                               userval=checkloggedin(session['userid']))


@app.route('/ziiei/<pagename>')
def workflow(pagename):
    if 'LanguageID' not in session:
        session['LanguageID'] = 1
    if 'RoleID' not in session:
        session['RoleID'] = 0
    if 'userid' not in session:
        session['userid'] = 0

    if pagename == 'workflow':
        return render_template('workflow.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray,
                               userval=checkloggedin(session['userid']))
    elif pagename == 'apply':
        return render_template('apply.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray,
                               userval=checkloggedin(session['userid']))
    elif pagename == 'benefits':
        return render_template('benefits.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray,
                               userval=checkloggedin(session['userid']))
    elif pagename == 'examples':
        return render_template('examples.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray,
                               userval=checkloggedin(session['userid']))
    elif pagename == 'terms':
        return render_template('terms.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray,
                               userval=checkloggedin(session['userid']))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.pop('userid', None)
    session.pop('RoleID', None)
    return redirect(url_for('index'))


@app.route('/contact')
def contact():
    return render_template('enquiry.html', topmenu=topmenu,
                           topsubmenu=topsubmenu, menuarray=menuarray,
                           userval=checkloggedin(session['userid']))


@app.route('/faq')
def faq():
    return render_template('faq.html', topmenu=topmenu,
                           topsubmenu=topsubmenu, menuarray=menuarray,
                           userval=checkloggedin(session['userid']))


@app.route('/register', methods=['GET','POST'])
def register():
    if 'username' in session:
        return redirect(url_for('index'))
    if 'LanguageID' not in session:
        session['LanguageID'] = masterlang
    if 'RoleID' not in session:
        session['RoleID'] = 0
    if 'userid' not in session:
        session['userid'] = 0
    if request.method == 'GET':
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
        return render_template('register.html', topmenu=topmenu,
                               topsubmenu=topsubmenu,
                               menuarray=menuarray, country=country, state=state,
                               district=district, block=block, clist=countrylist,
                               slist=statelist, dlist=districtdict, label=label_dict)
    else:
        countrylist = {}
        for single_country in country:
            statelist = []
            for single_state in state:
                if single_state[1] == single_country[1]:
                    statelist.append([single_state[3], single_state[2]])
            countrylist[single_country[1]] = statelist
        name = request.form['10']
        emp_id = request.form['11']
        DOB = request.form['12']
        quali = request.form['13']
        gender = request.form.get('14', '')
        DOJ = request.form['17']
        awards = request.form['18']
        address = request.form['19']
        phone = request.form['20']
        email = request.form['21']
        sch_name = request.form['22']
        designation = request.form['23']
        subjects = request.form['24']
        sch_addr = request.form['25']
        countryval = request.form['26']
        stateval = request.form['27']
        districtval = request.form['28']
        blockval = request.form['29']
        print(name)
        print(emp_id)
        print(DOB)
        print(quali)
        print(gender)
        print(DOJ)
        print(awards)
        print(address)
        print(phone)
        print(email)
        print(sch_name)
        print(designation)
        print(subjects) 
        print(sch_addr)
        print(countryval)
        print(stateval)
        print(districtval)
        print(blockval)

        return "dvfkvekv"


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
        return redirect(url_for('index'))
    if request.method == 'GET':
        label_dict = {}
        for label in labels:
            if label[1] == session['LanguageID'] and label[2] == session['RoleID'] and label[3] == '/submit':
                label_dict[label[0]] = label[5]
        benefits = values.benefit()
        stages = values.stage()
        bene_dict = {}
        for ben in benefits:
            bene_dict[ben[0]] = ben[1]
        stage_dict = {}
        for stag in stages:
            stage_dict[stag[0]] = stag[1]
        return render_template('submit.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, userval=checkloggedin(
                                   session['userid']), menuarray=menuarray, label=label_dict,
                               benefit=bene_dict,stage=stage_dict)
    else:
        pass


@app.route('/review')
def review():
    if 'username' not in session:
        return render_template('messages.html', label=labelval, menu=menuval,
                               submenu=submenuval, userval=checkloggedin(
                                   session['userid']),
                               message="You are not logged in!")

    return render_template('review.html', label=labelval, menu=menuval,
                           submenu=submenuval)

@app.route('/language/<int:langid>')
def language(langid):
    session.pop('LanguageID', None)
    session['LanguageID'] = langid
    return "polpol:("

if __name__ == '__main__':
    print("Fetching data...")
    labels = values.gettablevalues('Label')
    menus = values.gettablevalues('Menu')
    submenus = values.gettablevalues('SubMenu')
    categories = values.gettablevalues('Category')
    subcategories = values.gettablevalues('SubCategory')
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
    languages = values.gettablevalues('Language')
    for lang in languages:
        if lang[2] == 1:
            masterlang = lang[0]
            break
    country = values.gettablevalues('Country')
    state = values.gettablevalues('State')
    district = values.gettablevalues('District')
    block = values.gettablevalues('Block')
    print("Data fetched successfully!")
    app.run(debug=True, host='0.0.0.0', port=3000)
