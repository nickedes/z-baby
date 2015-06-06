import os
from flask import (
    Flask,
    render_template,
    session,
    url_for,
    redirect,
    request
)
from datetime import datetime
from errors import showerrors
import values
from werkzeug import secure_filename
import pyimgur


app = Flask(__name__)
app.secret_key = os.urandom(24)

showerrors(app)


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

    message = request.args.get('msg')
    return render_template('slash.html', topmenu=topmenu, menubody=menubody,
                            topsubmenu=topsubmenu, label=label_dict,
                           menuarray=menuarray, message=message)


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
        message = request.args.get('msg')
        return render_template('signin.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, message=message,
                               menuarray=menuarray, label=label_dict)
    else:
        if 'signin' in request.form:
            username = request.form['username']
            logged_in_val = values.checkLogin(
                request.form['username'], request.form['password'])
            print(logged_in_val)
            if logged_in_val is None:
                return redirect('/login?msg=Incorrect%20username%20or%20password!')

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
        return redirect('/login?msg=You%20are%20not%20logged%20in!')

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
                               topsubmenu=topsubmenu, menuarray=menuarray)
    elif pagename == 'sas':
        return render_template('sas.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray)
    elif pagename == 'litchi':
        return render_template('litchi.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray)
    elif pagename == 'upgovt':
        return render_template('upgovt.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray)


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
                               topsubmenu=topsubmenu, menuarray=menuarray)
    elif pagename == 'apply':
        return render_template('apply.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray)
    elif pagename == 'benefits':
        return render_template('benefits.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray)
    elif pagename == 'examples':
        return render_template('examples.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray)
    elif pagename == 'terms':
        return render_template('terms.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.pop('userid', None)
    session.pop('RoleID', None)
    return redirect(url_for('index'))


@app.route('/contact')
def contact():
    return render_template('enquiry.html', topmenu=topmenu,
                           topsubmenu=topsubmenu, menuarray=menuarray)


@app.route('/faq')
def faq():
    return render_template('faq.html', topmenu=topmenu,
                           topsubmenu=topsubmenu, menuarray=menuarray)


@app.route('/register', methods=['GET', 'POST'])
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
        phone = int(request.form['20'])
        altphone = int(request.form['53'])
        email = request.form['21']
        sch_name = request.form['22']
        designation = request.form['23']
        subjects = request.form['24']
        sch_addr = request.form['25']
        countryval = int(request.form['26'])
        stateval = int(request.form['27'])
        districtval = int(request.form['28'])
        blockval = int(request.form['29'])
        insertvals = values.insertvalues(name, DOB, sch_name, sch_addr, phone, altphone, DOJ, awards, emp_id, quali, gender,
                                         address, email, designation, subjects, blockval, districtval, stateval, countryval, "teacher-" + name, datetime.now())
        if insertvals == True:
            return redirect('/login?msg=Please%20sign%20in%20using%20your%20Employee%20ID%20as%20username%20and%20OTP%20as%20Password.')
        return redirect('/?msg=Something%20went%20wrong!%20Please%20try%20again%20later.')


@app.route('/update', methods=['GET', 'POST'])
def update():
    if 'username' not in session:
        return redirect(url_for('index'))
    if request.method == 'GET':
        label_dict = {}
        for label in labels:
            if label[1] == session['LanguageID'] and label[2] == session['RoleID'] and label[3] == '/update':
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

        teachers = values.teacherUnderOperator(session['userid'])
        details = values.getRegisteration_details(session['userid'])

        return render_template('update_register.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, teachers=teachers,
                               menuarray=menuarray, country=country, state=state,
                               district=district, block=block, clist=countrylist,
                               slist=statelist, dlist=districtdict, label=label_dict, detail=details[0])
    return render_template('update.html', topmenu=topmenu,
                           topsubmenu=topsubmenu,
                           menuarray=menuarray)


def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if 'username' not in session:
        return redirect('/login?msg=You%20are%20not%20logged%20in!')


    if request.method == 'GET':
        label_dict = {}
        for label in labels:
            if label[1] == session['LanguageID'] and label[2] == session['RoleID'] and label[3] == '/submit':
                label_dict[label[0]] = label[5]
        benefits = values.gettablevalues('Benefit')
        stages = values.gettablevalues('Stage')
        category = values.gettablevalues('Category')
        subcat = values.gettablevalues('SubCategory')
        bene_dict = {}
        for ben in benefits:
            if ben[0] == session['LanguageID']:
                bene_dict[ben[1]] = ben[2]
        stage_dict = {}
        for stag in stages:
            if stag[0] == session['LanguageID']:
                stage_dict[stag[1]] = stag[2]
        category_dict = {}
        for cat in category:
            if cat[0] == session['LanguageID']:
                category_dict[cat[1]] = cat[2]
        subcat_dict = {}
        for cat in category:
            sublist = []
            for sub in subcat:
                if sub[1] == cat[1]:
                    sublist.append([sub[3], sub[2]])
            subcat_dict[cat[1]] = sublist
        print(subcat_dict)
        return render_template('submit.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray, label=label_dict,
                               benefit=bene_dict, stage=stage_dict, category=category_dict, subcategory=subcat_dict)
    else:
        title = request.form['31']
        stage_id = request.form['33']
        benefit_id = request.form['34']
        category_id = request.form['36']
        subcategory_id = request.form['37']
        description = request.form['38']
        file = request.files['file']
        resource = request.form['42']
        support = request.form['44']
        implement_time = request.form['46']
        reach = request.form['47']
        example = request.form['49']
        UPLOAD_FOLDER = '/home/nickedes/zie_uploads'
        ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        medias = {}
        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            PATH = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(PATH)
            CLIENT_ID = values.getClient_ID()
            im = pyimgur.Imgur(CLIENT_ID)
            uploaded_image = im.upload_image(
                PATH, title="Uploaded with PyImgur")
            os.remove(PATH)
            image_link = uploaded_image.link
            medias['image'] = image_link
            print("file uploaded")
        IdeaID = values.getLatestIdea() + 1
        LoginID = session['userid']
        # "IdeaID, LoginID, title, stage, benefit, desc, resource, support, time, reach, cr_by, cr_date"
        insert = values.insertIdea(IdeaID, LoginID, title, stage_id, benefit_id,
                                   description, resource, support, implement_time, reach, LoginID, datetime.now())
        MediaID = values.getLatestMedia() + 1
        example = values.insertMedia(
            MediaID, IdeaID, 'image', medias['image'], LoginID, datetime.now())
        if insert == True and example == True:
            return "done"
        return redirect(url_for('/submit'))


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if 'username' not in session:
        return redirect('/login?msg=You%20are%20not%20logged%20in!')
    if request.method == 'GET':
        if session['RoleID'] == 4:
            dropdown = ['Category', 'SubCategory', 'Menu', 'SubMenu',
                        'Country', 'Block', 'District', 'State', 'Benefit', 'Stage']
        elif session['RoleID'] == 5:
            dropdown = [table[2] for table in tables]
        column_names = {}
        for dropdown_single in dropdown:
            column_names[dropdown_single] = values.getColumns(dropdown_single)
            column_names[1] = values.gettablevalues(dropdown_single)
        return render_template('edit.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray, dropdown=dropdown)
    else:
        if 'add' in request.form:
            pass
        elif 'edit' in request.form:
            pass
        elif 'delete' in request.form:
            pass


@app.route('/review')
def review():
    if 'username' not in session:
        return redirect('/login?msg=You%20are%20not%20logged%20in!')

    return render_template('review.html', label=labelval, menu=menuval,
                           submenu=submenuval)


@app.route('/language/<int:langid>')
def language(langid):
    session.pop('LanguageID', None)
    session['LanguageID'] = langid
    return redirect(request.args.get('next') or url_for('index'))

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
    tables = values.gettablelist()
    print("Data fetched successfully!")
    app.run(debug=True, host='0.0.0.0', port=3000)
