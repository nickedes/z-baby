import os
from flask import (
    Flask,
    render_template,
    session,
    url_for,
    redirect,
    request,
    flash
)
from functools import wraps
from datetime import datetime
from errors import showerrors
import values
from werkzeug import secure_filename
import pyimgur


app = Flask(__name__)
app.secret_key = os.urandom(24)

showerrors(app)


@app.before_request
def lalloo():
    pass


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'userid' not in session or session['userid'] == 0:
            flash('You are not logged in!', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


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

    return render_template('slash.html', languages=languages, topmenu=topmenu, menubody=menubody,
                           topsubmenu=topsubmenu, label=label_dict,
                           menuarray=menuarray)


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
        return render_template('signin.html', languages=languages, topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray,
                               label=label_dict)
    else:
        if 'signin' in request.form:
            username = request.form['username']
            logged_in_val = values.checkLogin(
                request.form['username'], request.form['password'])
            print(logged_in_val)
            if logged_in_val is None:
                flash('Incorrect Username or Password!', 'danger')
                return redirect(url_for('login'))

            else:
                session['RoleID'] = logged_in_val[0][0]
                session['username'] = username
                session['userid'] = logged_in_val[0][1]
                flash('You have successfully logged in!', 'success')
                return redirect(url_for('home'))
        elif 'submit' in request.form:
            pass


@app.route('/home')
@login_required
def home():
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
                           menulist=menulist,
                           languages=languages)


@app.route('/about/<pagename>')
def about(pagename):
    if 'LanguageID' not in session:
        session['LanguageID'] = 1
    if 'RoleID' not in session:
        session['RoleID'] = 0
    if 'userid' not in session:
        session['userid'] = 0

    if pagename == 'ziiei':
        return render_template('ziiei.html', languages=languages, topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray)
    elif pagename == 'sas':
        return render_template('sas.html', languages=languages, topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray)
    elif pagename == 'litchi':
        return render_template('litchi.html', languages=languages, topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray)
    elif pagename == 'upgovt':
        return render_template('upgovt.html', languages=languages, topmenu=topmenu,
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
        return render_template('workflow.html', languages=languages, topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray)
    elif pagename == 'apply':
        return render_template('apply.html', languages=languages, topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray)
    elif pagename == 'benefits':
        return render_template('benefits.html', languages=languages, topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray)
    elif pagename == 'examples':
        return render_template('examples.html', languages=languages, topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray)
    elif pagename == 'terms':
        return render_template('terms.html', languages=languages, topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.pop('userid', None)
    session.pop('RoleID', None)
    return redirect(url_for('index'))


@app.route('/contact')
def contact():
    return render_template('enquiry.html', languages=languages, topmenu=topmenu,
                           topsubmenu=topsubmenu, menuarray=menuarray)


@app.route('/faq')
def faq():
    return render_template('faq.html', languages=languages, topmenu=topmenu,
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
                               topsubmenu=topsubmenu, languages=languages,
                               menuarray=menuarray, country=country, state=state,
                               district=district, block=block, clist=countrylist,
                               slist=statelist, dlist=districtdict, label=label_dict)
    else:
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
                                         address, email, designation, subjects, blockval, districtval, stateval, countryval, "admin", datetime.now())
        if insertvals:
            flash(
                'Please sign in using your Employee ID as Username and OTP as Password.', 'info')
            return redirect(url_for('login'))
        flash('Something went wrong! Please try again later!', 'danger')
        return redirect(url_for('index'))


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        label_dict = {}
        for label in labels:
            if label[1] == session['LanguageID'] and label[3] == '/register':
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
                               topsubmenu=topsubmenu, languages=languages,
                               menuarray=menuarray, country=country, state=state,
                               district=district, block=block, clist=countrylist,
                               slist=statelist, dlist=districtdict, label=label_dict)
    else:
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

        insertvals = values.insertvalues(name, DOB, sch_name, sch_addr, phone,
                                         altphone, DOJ, awards, emp_id, quali,
                                         gender, address, email, designation,
                                         subjects, blockval, districtval,
                                         stateval, countryval,
                                         session['userid'], datetime.now())
        if insertvals:
            flash(
                'Please sign in using your Employee ID as Username and OTP as Password.', 'info')
            return redirect(url_for('login'))
        flash('Something went wrong! Please try again later!', 'danger')
        return redirect(url_for('index'))


@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
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
        if session['RoleID'] == 1:
            details = values.getRegisteration_details(session['userid'])
        elif session['RoleID'] == 2:
            details = values.getReg_underoperator(session['userid'])
        return render_template('update_register.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, teachers=teachers,
                               menuarray=menuarray, country=country, state=state,
                               district=district, block=block, clist=countrylist,
                               slist=statelist, dlist=districtdict, label=label_dict,
                               languages=languages, details=details)
    else:
        teacher_id = None
        if 'teacher_id' in request.form:
            teacher_id = request.form['teacher_id']
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
        if session['RoleID'] == 1:
            updatevals = values.update_register(session['userid'], name, DOB,
                                                sch_name, sch_addr, phone,
                                                altphone, DOJ, awards, emp_id,
                                                quali, gender, address, email,
                                                designation, subjects, blockval,
                                                districtval, stateval, countryval)
        elif session['RoleID'] == 2:
            updatevals = values.update_register(teacher_id, name, DOB,
                                                sch_name, sch_addr, phone,
                                                altphone, DOJ, awards, emp_id,
                                                quali, gender, address, email,
                                                designation, subjects, blockval,
                                                districtval, stateval, countryval)
        if updatevals == True:
            flash('Updated Registration Details.', 'success')
            return redirect(url_for('home'))
        flash('Something went wrong! Please try again later.', 'danger')
        return redirect(url_for('home'))

    return render_template('update.html', topmenu=topmenu,
                           topsubmenu=topsubmenu,
                           menuarray=menuarray,
                           languages=languages)


def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    if request.method == 'GET':
        label_dict = {}
        for label in labels:
            if label[1] == session['LanguageID'] and label[3] == '/submit':
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
                    sublist.append([sub[3], sub[2], sub[1]])
            subcat_dict[cat[1]] = sublist
        teachers = values.teacherUnderOperator(session['userid'])
        return render_template('submit.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray,
                               teachers=teachers, languages=languages,
                               label=label_dict, benefit=bene_dict,
                               stage=stage_dict, category=category_dict,
                               subcategory=subcat_dict)
    else:
        title = request.form['31']
        stage_id = request.form['33']
        benefit_id = request.form['34']
        category_id = request.form['36']
        subcategory_id = request.form.getlist('37'+str(category_id))
        description = request.form['38']

        resource = request.form['42']
        support = request.form['44']
        implement_time = request.form['46']
        reach = request.form['47']
        example = request.form['49']
        image_link = None
        try:
            file = request.files['file']
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
                print("done upload")
        except:
            pass
        IdeaID = values.getLatestIdea() + 1
        if session['RoleID'] == 1:
            LoginID = session['userid']
        elif session['RoleID'] == 2:
            Username = request.form['teacher']
            LoginID = values.getLoginID(Username)
            print(LoginID)
        insert = values.insertIdea(IdeaID, LoginID, title, stage_id, benefit_id,
                                   description, resource, support, implement_time, reach, session['userid'], datetime.now())
        if image_link:
            MediaID = values.getLatestMedia() + 1
            example_img = values.insertMedia(
                MediaID, IdeaID, medias['image'], 'image', session['userid'], datetime.now())
            print("done img")
        else:
            example_img = True
        MediaID = values.getLatestMedia() + 1
        example_text = values.insertMedia(
            MediaID, IdeaID, example, 'text', session['userid'], datetime.now())
        print("done exm")
        ideacatsubcat = values.insertIdeaCatSubCat(
            IdeaID, category_id, subcategory_id)
        if insert == True and example_text == True and example_img == True and ideacatsubcat == True:
            flash('The idea has been submitted successfully!', 'success')
            return redirect(url_for('home'))
        flash(
            'There was an error while submitting! Please try again!', 'danger')
        return redirect(url_for('submit'))


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'GET':
        if session['RoleID'] == 4:
            dropdown = ['Category', 'SubCategory', 'Menu', 'SubMenu',
                        'Country', 'Block', 'District', 'State', 'Benefit', 'Stage']
        elif session['RoleID'] == 5:
            dropdown = [table[2] for table in tables]
        column_names = {}
        for dropdown_single in dropdown:
            column_names[dropdown_single] = values.getColumns(dropdown_single)
        return render_template('edit.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray,
                               languages=languages, tables=dropdown)
    else:
        table = request.form['table']
        if session['RoleID'] == 5:
            filename = 'super_' + table.lower() + '.html'
            data = values.gettablevalues(table)
            cols = values.getColumns(table)
            return render_template(filename, topmenu=topmenu, languages=languages,
                                   topsubmenu=topsubmenu, menuarray=menuarray, table=data, header=cols)
        if session['RoleID'] == 4:
            if table == 'Category':
                data = values.gettablevalues('Category')
                cols = values.getColumns('Category')
                print(data)
                return render_template('Category_table.html', topmenu=topmenu, languages=languages,
                                       topsubmenu=topsubmenu, menuarray=menuarray, table=data, header=cols)
            if table == 'SubCategory':
                data = values.gettablevalues('SubCategory')
                cols = values.getColumns('SubCategory')
                return render_template('SubCategory.html', topmenu=topmenu, languages=languages,
                                       topsubmenu=topsubmenu, menuarray=menuarray, table=data, header=cols)
            if table == 'Menu':
                data = values.gettablevalues('Menu')
                cols = values.getColumns('Menu')
                print(data)
                return render_template('Menu.html', topmenu=topmenu, languages=languages,
                                       topsubmenu=topsubmenu, menuarray=menuarray, table=data, header=cols)
            if table == 'SubMenu':
                data = values.gettablevalues('SubMenu')
                cols = values.getColumns('SubMenu')
                return render_template('SubMenu.html', topmenu=topmenu, languages=languages,
                                       topsubmenu=topsubmenu, menuarray=menuarray, table=data, header=cols)
            if table == 'Country':
                data = values.gettablevalues('Country')
                cols = values.getColumns('Country')
                return render_template('Country.html', topmenu=topmenu, languages=languages,
                                       topsubmenu=topsubmenu, menuarray=menuarray, table=data, header=cols)
            if table == 'State':
                data = values.gettablevalues('State')
                cols = values.getColumns('State')
                return render_template('State.html', topmenu=topmenu, languages=languages,
                                       topsubmenu=topsubmenu, menuarray=menuarray, table=data, header=cols)
            if table == 'District':
                data = values.gettablevalues('District')
                cols = values.getColumns('District')
                return render_template('District.html', topmenu=topmenu,
                                       topsubmenu=topsubmenu, menuarray=menuarray, table=data, header=cols)
            if table == 'Block':
                data = values.gettablevalues('Block')
                cols = values.getColumns('Block')
                return render_template('Block.html', topmenu=topmenu,
                                       topsubmenu=topsubmenu, menuarray=menuarray, table=data, header=cols)
        print(table)


@app.route('/table', methods=['GET', 'POST'])
@login_required
def table():
    if request.method == 'POST':
        table = request.form['table']
        if table == "Category":
            if request.form['submit'] == 'edit':
                CatID = request.form['id']
                value = request.form[str(CatID)]
                update = values.updateCat(CatID, value)
                if update:
                    flash('Edited successfully!', 'success')
                    return redirect(url_for('home'))
            elif request.form['submit'] == 'translate':
                if table == "Category":
                    CatID = request.form['id']
                    langid = request.form['language']
                    value = request.form[str(CatID)+'translate']
                update = values.insertCat(
                    CatID, langid, value, session['userid'])
                if update:
                    flash('Translated successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was problem saving the translation! Please try again!', 'warning')
                return(redirect(url_for('home')))
        if table == "SubCategory":
            if request.form['submit'] == 'edit':
                CatID = request.form['CatID']
                SubCatID = request.form['SubCatID']
                value = request.form[str(SubCatID)]
                update = values.updateSubCat(CatID, SubCatID, value)
                if update:
                    flash('Edited successfully!', 'success')
                    return redirect(url_for('home'))
            elif request.form['submit'] == 'translate':
                CatID = request.form['id']
                SubCat = request.form['SubCatID']
                langid = request.form['language']
                value = request.form[str(SubCatID)+'translate']
                update = values.insertSubCat(
                    CatID, SubCatID, langid, value, session['userid'])
                if update:
                    flash('Translated successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was problem saving the translation! Please try again!', 'warning')
                return(redirect(url_for('home')))
        if table == "Menu":
            if request.form['submit'] == 'edit':
                MenuID = request.form['id']
                value = request.form[str(MenuID)]
                update = values.updateMenu(MenuID, value)
                if update:
                    flash('Edited successfully!', 'success')
                    return redirect(url_for('home'))
            elif request.form['submit'] == 'translate':
                MenuID = request.form['id']
                langid = request.form['language']
                value = request.form[str(MenuID)+'translate']
                for menu in menus:
                    if menu[1] == MenuID:
                        menuval = menu
                        break
                menuval[0] = langid
                menuval[3] = value
                menuval[6] = session['userid']
                menuval[7] = datetime.now()
                update = values.insertMenu(menuval)
                if update:
                    flash('Translated successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was problem saving the translation! Please try again!', 'warning')
                return(redirect(url_for('home')))
        if table == "SubMenu":
            if request.form['submit'] == 'edit':
                MenuID = request.form['MenuID']
                SubMenuID = request.form['SubMenuID']
                value = request.form[str(SubMenuID)]
                update = values.updateSubMenu(MenuID, SubMenuID, value)
                if update:
                    flash('Edited successfully!', 'success')
                    return redirect(url_for('home'))
            elif request.form['submit'] == 'translate':
                MenuID = request.form['id']
                SubMenuID = request.form['SubMenuID']
                langid = request.form['language']
                value = request.form[str(SubMenuID)+'translate']
                for submenu in submenus:
                    if submenu[1] == MenuID and submenu[2] == SubMenuID:
                        submenuval = submenu
                        break
                submenuval[0] = langid
                submenuval[4] = value
                submenuval[6] = session['userid']
                submenuval[7] = datetime.now()
                update = values.insertSubMenu(submenuval)
                if update:
                    flash('Translated successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was problem saving the translation! Please try again!', 'warning')
                return(redirect(url_for('home')))
        if table == "Country":
            if request.form['submit'] == 'edit':
                LangID = session['LanguageID']
                CountryID = request.form['id']
                value = request.form[str(CountryID)]
                update = values.updateCountry(LangID, CountryID, value)
                if update:
                    flash('Edited successfully!', 'success')
                    return redirect(url_for('home'))
            elif request.form['submit'] == 'translate':
                CountryID = request.form['id']
                langid = request.form['language']
                value = request.form[str(CountryID)+'translate']
                update = values.insertCountry(
                    langid, CountryID, value, session['userid'])
                if update:
                    flash('Translated successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was problem saving the translation! Please try again!', 'warning')
                return(redirect(url_for('home')))
        if table == "State":
            if request.form['submit'] == 'edit':
                LangID = session['LanguageID']
                CountryID = request.form['CountryID']
                StateID = request.form['StateID']
                value = request.form[str(StateID)]
                update = values.updateState(LangID, CountryID, StateID, value)
                if update:
                    flash('Edited successfully!', 'success')
                    return redirect(url_for('home'))
            elif request.form['submit'] == 'translate':
                CountryID = request.form['id']
                StateID = request.form['StateID']
                langid = request.form['language']
                value = request.form[str(StateID)+'translate']
                update = values.insertState(
                    langid, CountryID, StateID, value, session['userid'])
                if update:
                    flash('Translated successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was problem saving the translation! Please try again!', 'warning')
                return(redirect(url_for('home')))
        if table == "District":
            if request.form['submit'] == 'edit':
                LangID = session['LanguageID']
                CountryID = request.form['CountryID']
                StateID = request.form['StateID']
                DistrictID = request.form['DistrictID']
                value = request.form[str(DistrictID)]
                update = values.updateDistrict(
                    LangID, CountryID, StateID, DistrictID, value)
                if update:
                    flash('Edited successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was an error while editing! Please try again!', 'danger')
            elif request.form['submit'] == 'translate':
                CountryID = request.form['id']
                StateID = request.form['StateID']
                DistrictID = request.form['DistrictID']
                langid = request.form['language']
                value = request.form[str(DistrictID)+'translate']
                update = values.insertDistrict(
                    langid, CountryID, StateID, DistrictID, value, session['userid'])
                if update:
                    flash('Translated successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was problem saving the translation! Please try again!', 'warning')
                return(redirect(url_for('home')))
        if table == "Block":
            if request.form['submit'] == 'edit':
                LangID = session['LanguageID']
                CountryID = request.form['CountryID']
                StateID = request.form['StateID']
                DistrictID = request.form['DistrictID']
                BlockID = request.form['BlockID']
                value = request.form[str(BlockID)]
                update = values.updateBlock(
                    LangID, CountryID, StateID, DistrictID, BlockID, value)
                if update:
                    flash('Edited successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was an error while editing! Please try again!', 'danger')
            elif request.form['submit'] == 'translate':
                CountryID = request.form['id']
                StateID = request.form['StateID']
                DistrictID = request.form['DistrictID']
                BlockID = request.form['BlockID']
                langid = request.form['language']
                value = request.form[str(DistrictID)+'translate']
                update = values.insertBlock(
                    langid, CountryID, StateID, DistrictID, BlockID, value, session['userid'])
                if update:
                    flash('Translated successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was problem saving the translation! Please try again!', 'warning')
                return(redirect(url_for('home')))
        return redirect(url_for('edit'))


@app.route('/review', methods=['GET', 'POST'])
@login_required
def review():
    if request.method == 'GET':
        teachers = values.teacherUnderOperator(session['userid'])
        if session['RoleID'] == 1:
            idea_details = values.getIdeaInfo(session['userid'])
        elif session['RoleID'] == 2:
            idea_details = values.getIdeaUnderOperator(session['userid'])
        subcatidea = {}
        media = {}
        for idea_single in idea_details:
            subcatidea[idea_single[0]] = values.getIdeaCatSubCat(
                idea_single[0])
            media[idea_single[0]] = values.getMedia(idea_single[0])
        label_dict = {}
        for label in labels:
            if label[1] == session['LanguageID'] and label[3] == '/submit':
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
                    sublist.append([sub[3], sub[2], sub[1]])
            subcat_dict[cat[1]] = sublist
        sub_list = {}
        for data in subcatidea:
            sub_list[data] = []
            for y in subcatidea[data]:
                sub_list[data].append(y[2])
        print(subcatidea)
        return render_template('review.html', topmenu=topmenu,
                               topsubmenu=topsubmenu, menuarray=menuarray,
                               label=label_dict, benefit=bene_dict,
                               stage=stage_dict, category=category_dict, media=media, teachers=teachers,
                               subcategory=subcat_dict, ideas=idea_details, subcats=subcatidea,
                               languages=languages, sublist=sub_list)
    else:
        IdeaID = request.form['idea']
        title = request.form['31']
        stage_id = request.form['33']
        benefit_id = request.form['34']
        category_id = request.form['36']
        subcategory_id = request.form.getlist('37'+str(category_id))
        description = request.form['38']
        resource = request.form['42']
        support = request.form['44']
        implement_time = request.form['46']
        reach = request.form['47']
        example = request.form['49']

        image_link = None
        try:
            file = request.files['file']
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
                print("done upload")
        except:
            pass
        insert = values.updateIdea(IdeaID, title, stage_id, benefit_id,
                                   description, resource, support, implement_time, reach)
        if image_link:
            example_img = values.updateMedia(
                IdeaID, medias['image'], 'image', datetime.now())
            print("done img")
        else:
            example_img = True
        example_text = values.updateMedia(
            IdeaID, example, 'text', datetime.now())
        print("done exm")
        ideacatsubcat = values.updateIdeaCatSubCat(
            IdeaID, category_id, subcategory_id)
        if insert == True and example_text == True and example_img == True and ideacatsubcat == True:
            flash('The idea has been submitted successfully!', 'success')
            return redirect(url_for('home'))
        flash(
            'There was an error while submitting! Please try again!', 'danger')
        return redirect(url_for('review'))

    return render_template('review.html', topmenu=topmenu,
                           topsubmenu=topsubmenu, menuarray=menuarray,
                           languages=languages)


def upload_img(upload_file):
    file = upload_file
    UPLOAD_FOLDER = '/home/nickedes/zie_uploads'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
        filename = secure_filename(file.filename)
        PATH = os.path.join(
            app.config['UPLOAD_FOLDER'], filename)
        file.save(PATH)
        CLIENT_ID = values.getClient_ID()
        im = pyimgur.Imgur(CLIENT_ID)
        uploaded_image = im.upload_image(
            PATH, title="Uploaded with PyImgur")
        os.remove(PATH)
        print("done upload")
    return uploaded_image.link


@app.route('/super', methods=['GET', 'POST'])
@login_required
def super():
    # if session['userid'] == 5:
    if request.method == 'POST':
        table = request.form['table']
        if table == "Media":
            if request.form['submit'] == 'edit':
                print(request.form)
                MediaID = request.form['id']
                IdeaID = request.form[str(MediaID)]
                value = request.form[str(IdeaID)]
                Mtype = request.form['MediaType']
                update = values.SupdateMedia(MediaID, IdeaID, value, Mtype)
                if update:
                    flash('Edited successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was problem saving the Media! Please try again!', 'warning')
                return(redirect(url_for('home')))
            elif request.form['submit'] == 'delete':
                MediaID = request.form['id']
                IdeaID = request.form[str(MediaID)]
                delete = values.deleteMedia(MediaID, IdeaID)
                if delete:
                    flash('Media Deleted successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was problem deleting the Media! Please try again!', 'warning')
            elif request.form['submit'] == 'image':
                IdeaID = request.form['id']
                if values.NoIdea(IdeaID):
                    flash(
                        'No Such Idea exists, for which you are adding Media. Please try again!', 'warning')
                    return(redirect(url_for('home')))
                print("in")
                image_link = None
                image_link = upload_img(request.files['file'])
                if image_link:
                    MediaID = values.getLatestMedia() + 1
                    example_img = values.insertMedia(
                        MediaID, IdeaID, image_link, 'image', session['userid'], datetime.now())
                    print("done img")
                    if example_img:
                        flash('Media Added successfully!', 'success')
                        return redirect(url_for('home'))
                flash(
                    'There was problem adding the Media! Please try again!', 'warning')
                return(redirect(url_for('home')))

            elif request.form['submit'] == 'text':
                IdeaID = request.form['id']
                if values.NoIdea(IdeaID):
                    flash(
                        'No Such Idea exists, for which you are adding Media. Please try again!', 'warning')
                    return(redirect(url_for('home')))
                example = request.form['example']
                MediaID = values.getLatestMedia() + 1
                example_text = values.insertMedia(
                    MediaID, IdeaID, example, 'text', session['userid'], datetime.now())
                print("done exm")
                if example_text:
                    flash('Media Added successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was problem adding the Media! Please try again!', 'warning')
                return(redirect(url_for('home')))

            else:
                pass

        elif table == 'Country':
            if request.form['submit'] == 'edit':
                LangID = session['LanguageID']
                CountryID = request.form['id']
                value = request.form[str(CountryID)]
                update = values.updateCountry(LangID, CountryID, value)
                if update:
                    flash('Edited successfully!', 'success')
                    return redirect(url_for('home'))

            elif request.form['submit'] == 'delete':
                LangID = session['LanguageID']
                CountryID = request.form['id']
                if values.CheckCountry(CountryID):
                    flash(
                        "This Country Can't be deleted,since it has states", 'warning')
                    return(redirect(url_for('home')))
                delete = values.deleteCountry(LangID, CountryID)
                if delete:
                    flash('Country Deleted successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was problem deleting the Country! Please try again!', 'warning')

            elif request.form['submit'] == 'translate':
                CountryID = request.form['id']
                langid = request.form['language']
                value = request.form[str(CountryID)+'translate']
                update = values.insertCountry(
                    langid, CountryID, value, session['userid'])
                if update:
                    flash('Translated successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was problem saving the translation! Please try again!', 'warning')
                return(redirect(url_for('home')))

            elif request.form['submit'] == 'add':
                CountryID = values.getCountryID()+1
                LangID = session['LanguageID']
                name = request.form['name']
                insert = values.insertCountry(
                    LangID, CountryID, name, session['userid'])
                if insert:
                    flash('Country Added successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was problem adding the Country! Please try again!', 'warning')
                return(redirect(url_for('home')))

        elif table == 'State':
            if request.form['submit'] == 'edit':
                LangID = session['LanguageID']
                CountryID = request.form['CountryID']
                StateID = request.form['StateID']
                value = request.form[str(StateID)]
                update = values.updateState(LangID, CountryID, StateID, value)
                if update:
                    flash('Edited successfully!', 'success')
                    return redirect(url_for('home'))

            elif request.form['submit'] == 'delete':
                LangID = session['LanguageID']
                CountryID = request.form['CountryID']
                StateID = request.form['StateID']
                if values.CheckState(StateID):
                    flash(
                        "This State Can't be deleted,since it has districts", 'warning')
                    return(redirect(url_for('home')))
                delete = values.deleteState(LangID, CountryID, StateID)
                if delete:
                    flash('State Deleted successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was problem deleting the State! Please try again!', 'warning')

            elif request.form['submit'] == 'translate':
                CountryID = request.form['id']
                StateID = request.form['StateID']
                langid = request.form['language']
                value = request.form[str(StateID)+'translate']
                update = values.insertState(
                    langid, CountryID, StateID, value, session['userid'])
                if update:
                    flash('Translated successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was problem saving the translation! Please try again!', 'warning')
                return(redirect(url_for('home')))

            elif request.form['submit'] == 'add':
                CountryID = request.form['CID']
                if values.NoCountry(CountryID):
                    flash(
                        'No Such Country exists, for which you are adding State. Please try again!', 'warning')
                    return(redirect(url_for('home')))
                LangID = session['LanguageID']
                name = request.form['name']
                StateID = values.getStateID(CountryID) + 1
                insert = values.insertState(
                    LangID, CountryID, StateID, name, session['userid'])
                if insert:
                    flash('State Added successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was problem adding the State! Please try again!', 'warning')
                return(redirect(url_for('home')))
            else:
                pass

        elif table == 'District':
            if request.form['submit'] == 'edit':
                LangID = session['LanguageID']
                CountryID = request.form['CountryID']
                StateID = request.form['StateID']
                DistrictID = request.form['DistrictID']
                value = request.form[str(DistrictID)]
                update = values.updateDistrict(
                    LangID, CountryID, StateID, DistrictID, value)
                if update:
                    flash('Edited successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was an error while editing! Please try again!', 'danger')
            elif request.form['submit'] == 'delete':
                DistrictID = request.form['DistrictID']
                if values.CheckDistrict(DistrictID):
                    flash(
                        "This District Can't be deleted,since it has blocks", 'warning')
                    return(redirect(url_for('home')))
                delete = values.deleteDistrict(
                    LangID, CountryID, StateID, DistrictID)
                if delete:
                    flash('District Deleted successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was problem deleting the District! Please try again!', 'warning')

            elif request.form['submit'] == 'add':
                CountryID = request.form['CID']
                if values.NoCountry(CountryID):
                    flash(
                        'No Such Country exists, for which you are adding State. Please try again!', 'warning')
                    return(redirect(url_for('home')))
                StateID = request.form['SID']
                if values.NoState(StateID):
                    flash(
                        'No Such State exists, for which you are adding District. Please try again!', 'warning')
                    return(redirect(url_for('home')))
                LangID = session['LanguageID']
                name = request.form['name']
                DistrictID = values.getDistrictID(CountryID, StateID) + 1
                insert = values.insertDistrict(
                    LangID, CountryID, StateID, DistrictID, name, session['userid'])
                if insert:
                    flash('District Added successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was problem adding the District! Please try again!', 'warning')
                return(redirect(url_for('home')))
            else:
                pass

        elif table == 'Block':
            if request.form['submit'] == 'edit':
                LangID = session['LanguageID']
                CountryID = request.form['CountryID']
                StateID = request.form['StateID']
                DistrictID = request.form['DistrictID']
                BlockID = request.form['BlockID']
                value = request.form[str(BlockID)]
                update = values.updateDistrict(
                    LangID, CountryID, StateID, DistrictID, BlockID, value)
                if update:
                    flash('Block Edited successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was an error while editing! Please try again!', 'danger')
            elif request.form['submit'] == 'delete':
                BlockID = request.form['BlockID']
                delete = values.deleteBlock(
                    LangID, CountryID, StateID, DistrictID, BlockID)
                if delete:
                    flash('Block Deleted successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was problem deleting the Block! Please try again!', 'warning')

            elif request.form['submit'] == 'add':
                CountryID = request.form['CID']
                if values.NoCountry(CountryID):
                    flash(
                        'No Such Country exists, for which you are adding State. Please try again!', 'warning')
                    return(redirect(url_for('home')))
                StateID = request.form['SID']
                if values.NoState(StateID):
                    flash(
                        'No Such State exists, for which you are adding District. Please try again!', 'warning')
                    return(redirect(url_for('home')))
                LangID = session['LanguageID']
                name = request.form['name']
                DistrictID = values.getDistrictID(CountryID, StateID) + 1
                insert = values.insertDistrict(
                    LangID, CountryID, StateID, DistrictID, name, session['userid'])
                if insert:
                    flash('District Added successfully!', 'success')
                    return redirect(url_for('home'))
                flash(
                    'There was problem adding the District! Please try again!', 'warning')
                return(redirect(url_for('home')))
            else:
                pass

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
    languages = values.gettablevalues('Language')
    print("Data fetched successfully!")
    app.run(debug=True, host='0.0.0.0', port=3000)
