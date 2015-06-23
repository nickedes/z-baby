import os
from flask import (
    Flask,
    render_template,
    session,
    url_for,
    redirect,
    request,
    flash,
    g
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
    if 'LanguageID' not in session:
        session['LanguageID'] = masterlang
    topmenu = []
    topsubmenu = []
    menuarray = [0 for menu in menus if menu[5]
                 == -1 and menu[0] == session['LanguageID']]
    for menu in menus:
        if menu[5] == -1 and menu[0] == session['LanguageID']:
            topmenu.append([menu[3], menu[4], menu[1]])
        for submenu in submenus:
            if submenu[5] == -1 and submenu[1] == menu[1] and submenu[0] == session['LanguageID'] and menu[0] == session['LanguageID']:
                menuarray[submenu[1]-1] = 1
                topsubmenu.append([submenu[1], submenu[3], submenu[4]])
    g.languages = languages
    g.topmenu = topmenu
    g.topsubmenu = topsubmenu
    g.menuarray = menuarray
    g.masterlang = masterlang


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
        if label[1] == session['LanguageID'] and label[2] == session['RoleID']\
                and label[3] == '/':
            label_dict[label[0]] = label[5]

    menubody = []
    for menu in menus:
        if menu[5] == session['RoleID'] and menu[0] == session['LanguageID'] \
                and menu[2] == '/':
            menubody.append([menu[3], menu[4]])

    return render_template('slash.html', menubody=menubody, label=label_dict)


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
            if label[1] == session['LanguageID'] and label[2] == \
                    session['RoleID'] and label[3] == '/login':
                label_dict[label[0]] = label[5]
        return render_template('signin.html', label=label_dict)
    else:
        if 'signin' in request.form:
            username = request.form['username']
            logged_in_val = values.checkLogin(
                request.form['username'], request.form['password'])
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
        if label[1] == session['LanguageID'] and label[2] == session['RoleID']\
                and label[3] == '/home':
            label_dict[label[0]] = label[5]
    menulist = []
    for menu in menus:
        if menu[0] == session['LanguageID'] and menu[2] == '/home' and menu[5] == session['RoleID']:
            menulist.append([menu[3], menu[4]])
    inno = values.checkInnovation(session['userid'])
    return render_template('home.html', inno=inno, label=label_dict, menulist=menulist)


@app.route('/about/<pagename>')
def about(pagename):
    if 'LanguageID' not in session:
        session['LanguageID'] = 1
    if 'RoleID' not in session:
        session['RoleID'] = 0
    if 'userid' not in session:
        session['userid'] = 0

    if pagename == 'ziiei':
        return render_template('ziiei.html')
    elif pagename == 'sas':
        return render_template('sas.html')
    elif pagename == 'litchi':
        return render_template('litchi.html')
    elif pagename == 'upgovt':
        return render_template('upgovt.html')


@app.route('/ziiei/<pagename>')
def workflow(pagename):
    if 'LanguageID' not in session:
        session['LanguageID'] = 1
    if 'RoleID' not in session:
        session['RoleID'] = 0
    if 'userid' not in session:
        session['userid'] = 0

    if pagename == 'workflow':
        return render_template('workflow.html')
    elif pagename == 'apply':
        return render_template('apply.html')
    elif pagename == 'benefits':
        return render_template('benefits.html')
    elif pagename == 'examples':
        return render_template('examples.html')
    elif pagename == 'terms':
        return render_template('terms.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.pop('userid', None)
    session.pop('RoleID', None)
    return redirect(url_for('index'))


@app.route('/contact')
def contact():
    return render_template('enquiry.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


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
        return render_template('register.html', country=country, state=state,
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
    """Dataentry operator method for creating teacher profiles"""
    if session['RoleID'] != 2:
        flash(
            'Sorry, you are not authorised to access this function', 'danger')
        return redirect(url_for('home'))
    if request.method == 'GET':
        label_dict = {}
        for label in labels:
            if label[1] == session['LanguageID'] and label[3] == '/register':
                label_dict[label[0]] = [label[4], label[5]]
        countrylist = {}
        for single_country in country:
            statelist = []
            if single_country[0] == session['LanguageID']:
                for single_state in state:
                    if single_state[0] == session['LanguageID'] and single_state[1] == single_country[1]:
                        statelist.append([single_state[3], single_state[2]])
                countrylist[single_country[1]] = statelist
        statelist = {}
        for single_state in state:
            districtlist = []
            if single_state[0] == session['LanguageID']:
                for single_district in district:
                    if single_district[2] == single_state[2] and single_district[0] == session['LanguageID']:
                        districtlist.append(
                            [single_district[4], single_district[3]])
                statelist[single_state[2]] = districtlist
        districtdict = {}
        for single_district in district:
            blocklist = []
            if single_district[0] == session['LanguageID']:
                for single_block in block:
                    if single_block[3] == single_district[3]:
                        blocklist.append([single_block[5], single_block[4]])
                districtdict[single_district[3]] = blocklist

        return render_template('register.html', country=country, state=state,
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
                'A new teacher profile created.', 'info')
            return redirect(url_for('login'))
        flash('Something went wrong! Please try again later!', 'danger')
        return redirect(url_for('index'))


@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    """Updating profiles for teacher and dataentry operators"""
    if session['RoleID'] > 2:
        flash(
            'Sorry, you are not authorised to access this function', 'danger')
        return redirect(url_for('home'))
    if request.method == 'GET':
        label_dict = {}
        for label in labels:
            if label[1] == session['LanguageID'] and label[2] == session['RoleID'] and label[3] == '/update':
                label_dict[label[0]] = [label[4], label[5]]
        countrylist = {}
        for single_country in country:
            statelist = []
            if single_country[0] == session['LanguageID']:
                for single_state in state:
                    if single_state[0] == session['LanguageID'] and single_state[1] == single_country[1]:
                        statelist.append([single_state[3], single_state[2]])
                countrylist[single_country[1]] = statelist
        statelist = {}
        for single_state in state:
            districtlist = []
            if single_state[0] == session['LanguageID']:
                for single_district in district:
                    if single_district[2] == single_state[2] and single_district[0] == session['LanguageID']:
                        districtlist.append(
                            [single_district[4], single_district[3]])
                statelist[single_state[2]] = districtlist
        districtdict = {}
        for single_district in district:
            blocklist = []
            if single_district[0] == session['LanguageID']:
                for single_block in block:
                    if single_block[3] == single_district[3]:
                        blocklist.append([single_block[5], single_block[4]])
                districtdict[single_district[3]] = blocklist
        teachers = values.teacherUnderOperator(session['userid'])
        if session['RoleID'] == 1:
            details = values.getRegisteration_details(session['userid'])
        elif session['RoleID'] == 2:
            details = values.getReg_underoperator(session['userid'])
        return render_template('update_register.html', teachers=teachers,
                               country=country, state=state, district=district,
                               block=block, clist=countrylist, slist=statelist,
                               dlist=districtdict, label=label_dict,
                               details=details)
    else:
        teacher_id = None
        print request.form
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

    return render_template('update.html')


def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    """ Idea submission for teachers and data entry operators"""
    if session['RoleID'] > 2:
        flash(
            'Sorry, you are not authorised to access this function', 'danger')
        return redirect(url_for('home'))
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
            if cat[0] == session['LanguageID']:
                for sub in subcat:
                    if sub[1] == cat[1] and sub[0] == session['LanguageID']:
                        sublist.append([sub[3], sub[2], sub[1]])
                subcat_dict[cat[1]] = sublist
        teachers = values.teacherUnderOperator(session['userid'])
        return render_template('submit.html', teachers=teachers,
                               label=label_dict, benefit=bene_dict,
                               stage=stage_dict, category=category_dict,
                               subcategory=subcat_dict)
    else:
        print request.files
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
        # try:
        file = request.files['file']
        UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
        ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','PNG','JPG','JPEG'])
        ALLOWED_EXTENSIONS_VIDEO = set(['mp4'])
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

    IdeaID = values.getLatestIdea() + 1
    if session['RoleID'] == 1:
        LoginID = session['userid']
    elif session['RoleID'] == 2:
        Username = request.form['teacher']
        LoginID = values.getLoginID(Username)
    insert = values.insertIdea(IdeaID, LoginID, title, stage_id, benefit_id,
                               description, resource, support, implement_time, reach, session['userid'], datetime.now())
    if image_link:
        MediaID = values.getLatestMedia() + 1
        example_img = values.insertMedia(
            MediaID, IdeaID, medias['image'], 'image', session['userid'], datetime.now())
    else:
        example_img = True
    MediaID = values.getLatestMedia() + 1
    example_text = values.insertMedia(
        MediaID, IdeaID, example, 'text', session['userid'], datetime.now())
    ideacatsubcat = values.insertIdeaCatSubCat(
        IdeaID, category_id, subcategory_id,session['userid'],datetime.now())
    if insert == True and example_text == True and example_img == True and ideacatsubcat == True:
        flash('The idea has been submitted successfully!', 'success')
        return redirect(url_for('home'))
    flash(
        'There was an error while submitting! Please try again!', 'danger')
    return redirect(url_for('submit'))


@app.route('/view')
@login_required
def view():
    """View Innovations by RoleID = 3"""
    if session['RoleID'] != 3:
        flash('Sorry, you are not authorised to access this function', 'danger')
        return redirect(url_for('home'))
    data = []
    if 'value' not in request.args:
        data = ideas
    else:
        value = request.args.get('value')
        field = request.args.get('field')

        for idea in ideas:
            if idea[field].find(value) != -1:
                data.append(idea)
    header = values.getColumns('Idea')


    return render_template('view.html', header=header, table=data)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    """Table editing for admin and superadmin"""
    if session['RoleID'] < 4:
        flash(
            'Sorry, you are not authorised to access this function', 'danger')
        return redirect(url_for('home'))
    if request.method == 'GET':
        if session['RoleID'] == 4:
            dropdown = ['Category', 'SubCategory', 'Menu', 'SubMenu', 'Label',
                        'Country', 'Block', 'District', 'State', 'Benefit', 'Stage']
        elif session['RoleID'] == 5:
            dropdown = [table[2] for table in tables]
        column_names = {}
        for dropdown_single in dropdown:
            column_names[dropdown_single] = values.getColumns(dropdown_single)
        return render_template('edit.html', tables=dropdown)
    else:
        table = request.form['table']
        if session['RoleID'] == 5:
            filename = 'super_' + table.lower() + '.html'
            data = values.gettablevalues(table)
            cols = values.getColumns(table)
            return render_template(filename, table=data, header=cols)
        elif session['RoleID'] == 4:
            data = values.gettablevalues(table)
            cols = values.getColumns(table)
            return render_template(table + ".html", table=data, header=cols)


@app.route('/table/<tablename>', methods=['GET', 'POST'])
@login_required
def table(tablename):
    if session['RoleID'] < 4:
        flash(
            'Sorry, you are not authorised to access this function', 'warning')
        return redirect(url_for('home'))
    if request.method == 'GET':
        if session['RoleID'] == 4:
            filename = tablename + '.html'
            data = values.gettablevalues(tablename)
            cols = values.getColumns(tablename)
            return render_template(filename, table=data, header=cols)
        flash(
            'You do not have the priviledge to access that function!', 'danger')
        return redirect(url_for('home'))

    elif request.method == 'POST':

        # First, decide on which language ID to use (since all admin editing
        # requires this)
        if request.form['submit'] == 'edit':
            langid = request.form['LangID']
        elif request.form['submit'] == 'translate':
            langid = request.form['language']

        # Then, decide which table it is we're editing
        if tablename == "Label":
            # When the table is clear, pick common elements
            LabelID = request.form['id']
            # Then, decide value based on whether admin wants to edit or
            # translate
            if request.form['submit'] == 'edit':
                value = request.form[str(LabelID)]
            elif request.form['submit'] == 'translate':
                value = request.form[str(LabelID)+'translate']
            # Update the values (store result in update for later!)
            update = values.updateLabel(LabelID, value, langid)
            global labels
            labels = values.gettablevalues('Label')

        if tablename == "Category":
            CatID = request.form['id']

            if request.form['submit'] == 'edit':
                value = request.form[str(CatID)]
            elif request.form['submit'] == 'translate':
                value = request.form[str(CatID)+'translate']

            update = values.updateCat(langid, CatID, value)
            global categories
            categories = values.gettablevalues('Category')

        if tablename == "SubCategory":
            CatID = request.form['CatID']
            SubCatID = request.form['SubCatID']

            if request.form['submit'] == 'edit':
                value = request.form[str(SubCatID)]
            elif request.form['submit'] == 'translate':
                value = request.form[str(SubCatID)+'translate']

            update = values.updateSubCat(langid, CatID, SubCatID, value)
            global subcategories
            subcategories = values.gettablevalues('SubCategory')

        if tablename == "Menu":
            MenuID = request.form['id']

            if request.form['submit'] == 'edit':
                value = request.form[str(MenuID)]
            elif request.form['submit'] == 'translate':
                value = request.form[str(MenuID)+'translate']

            update = values.updateMenu(langid, MenuID, value)
            global menus
            menus = values.gettablevalues('Menu')

        if tablename == "SubMenu":
            MenuID = request.form['MenuID']
            SubMenuID = request.form['SubMenuID']

            if request.form['submit'] == 'edit':
                value = request.form[str(SubMenuID)]
            elif request.form['submit'] == 'translate':
                value = request.form[str(SubMenuID)+'translate']

            update = values.updateSubMenu(langid, MenuID, SubMenuID, value)
            global submenus
            submenus = values.gettablevalues('SubMenu')

        if tablename == "Country":
            CountryID = request.form['id']

            if request.form['submit'] == 'edit':
                value = request.form[str(CountryID)]
            elif request.form['submit'] == 'translate':
                value = request.form[str(CountryID)+'translate']

            update = values.updateCountry(langid, CountryID, value)
            global country
            country = values.gettablevalues('Country')

        if tablename == "State":
            CountryID = request.form['CountryID']
            StateID = request.form['StateID']

            if request.form['submit'] == 'edit':
                value = request.form[str(StateID)]
            elif request.form['submit'] == 'translate':
                value = request.form[str(StateID)+'translate']

            update = values.updateState(langid, CountryID, StateID, value)
            global state
            state = values.gettablevalues('State')

        if tablename == "District":
            CountryID = request.form['CountryID']
            StateID = request.form['StateID']
            DistrictID = request.form['DistrictID']

            if request.form['submit'] == 'edit':
                value = request.form[str(DistrictID)]
            elif request.form['submit'] == 'translate':
                value = request.form[str(DistrictID)+'translate']

            update = values.updateDistrict(
                langid, CountryID, StateID, DistrictID, value)
            global district
            district = values.gettablevalues('District')

        if tablename == "Block":
            CountryID = request.form['CountryID']
            StateID = request.form['StateID']
            DistrictID = request.form['DistrictID']
            BlockID = request.form['BlockID']

            if request.form['submit'] == 'edit':
                value = request.form[str(BlockID)]
            elif request.form['submit'] == 'translate':
                value = request.form[str(DistrictID)+'translate']

            update = values.updateBlock(
                langid, CountryID, StateID, DistrictID, BlockID, value)
            global block
            block = values.gettablevalues('Block')

        if tablename == "Benefit":
            BenefitID = request.form['id']

            if request.form['submit'] == 'edit':
                value = request.form[str(BenefitID)]
            elif request.form['submit'] == 'translate':
                value = request.form[str(BenefitID)+'translate']

            update = values.updateBenefit(langid, BenefitID, value)
            global benefits
            benefits = values.gettablevalues('Benefit')

        if tablename == "Stage":
            StageID = request.form['id']

            if request.form['submit'] == 'edit':
                value = request.form[str(StageID)]
            elif request.form['submit'] == 'translate':
                value = request.form[str(StageID)+'translate']

            update = values.updateStage(langid, StageID, value)
            global stages
            stages = values.gettablevalues('Stage')
        # Check if the update was a success, and display message appropriately
        if update:
            flash('The ' + tablename + ' was successfully edited!', 'success')
        flash(
            'Sorry, there was an error while editing! Please try again!', 'danger')
        return redirect('/table/' + tablename)


@app.route('/review', methods=['GET', 'POST'])
@login_required
def review():
    """Review Ideas/Innovation for teachers and dataentry operators"""
    if session['RoleID'] != 1 and session['RoleID'] != 2:
        flash(
            'Sorry, you are not authorised to access this function', 'warning')
        return redirect(url_for('home'))
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
        for sub in subcat:
            subcat_dict[sub[1]] = []
        for sub in subcat:
            if [sub[3], sub[2], sub[1]] not in subcat_dict[sub[1]]:
                subcat_dict[sub[1]].append([sub[3], sub[2], sub[1]])

        sub_list = {}
        for data in subcatidea:
            sub_list[data] = []
            for y in subcatidea[data]:
                sub_list[data].append(y[2])

        return render_template('review.html', label=label_dict,
                               benefit=bene_dict, stage=stage_dict,
                               category=category_dict, media=media,
                               teachers=teachers, subcategory=subcat_dict,
                               ideas=idea_details, subcats=subcatidea,
                               sublist=sub_list)
    else:
        print request.form
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
            UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
            ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','PNG','JPG','JPEG'])
            ALLOWED_EXTENSIONS_VIDEO = set(['mp4'])
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
        except:
            pass
        insert = values.updateIdea(IdeaID, title, stage_id, benefit_id,
                                   description, resource, support, implement_time, reach)
        if image_link:
            if 'MediaID_img' in request.form:
                MediaID = request.form['MediaID_img']
                example_img = values.updateMedia(
                IdeaID, medias['image'], 'image', datetime.now(),MediaID)
            else:
                MediaID = values.getLatestMedia() + 1
                example_img = values.insertMedia(
                        MediaID, IdeaID, image_link, 'image', session['userid'], datetime.now())
        else:
            example_img = True
        MediaID = request.form['MediaID_ex']
        example_text = values.updateMedia(
            IdeaID, example, 'text', datetime.now(), MediaID)
        ideacatsubcat = values.updateIdeaCatSubCat(
            IdeaID, category_id, subcategory_id,session['userid'],datetime.now())
        if insert == True and example_text == True and example_img == True and ideacatsubcat == True:
            flash('The idea has been submitted successfully!', 'success')
            return redirect(url_for('home'))
        flash(
            'There was an error while submitting! Please try again!', 'danger')
        return redirect(url_for('review'))

    return render_template('review.html')


def upload_img(upload_file):
    file = upload_file
    UPLOAD_FOLDER = r'F:\\'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','PNG','JPG','JPEG'])
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
        filename = secure_filename(file.filename)
        PATH = os.path.join(
            app.config['UPLOAD_FOLDER'], filename)
        file.save(PATH)
        CLIENT_ID = values.getClient_ID()
        print CLIENT_ID
        im = pyimgur.Imgur(CLIENT_ID)
        print im
        uploaded_image = im.upload_image(
            PATH, title="Uploaded with PyImgur")
        os.remove(PATH)
    return uploaded_image.link


@app.route('/super/<tablename>', methods=['GET', 'POST'])
@login_required
def super(tablename):
    """ADD/EDIT/DELETE/VIEW for superadmin"""
    if session['RoleID'] != 5:
        flash(
            'Sorry, you are not authorised to access this function', 'danger')
        return redirect(url_for('home'))
    if request.method == 'GET':
        if session['RoleID'] == 5:
            filename = 'super_' + tablename.lower() + '.html'
            data = values.gettablevalues(tablename)
            cols = values.getColumns(tablename)
            return render_template(filename, table=data, header=cols)
        flash(
            'You do not have the priviledge to access that function!', 'danger')
        return redirect(url_for('home'))
    elif request.method == 'POST':
        table = request.form['table']
        if table == "Media":
            if request.form['submit'] == 'edit':
                MediaID = request.form['id']
                IdeaID = request.form[str(MediaID)]
                value = request.form[str(IdeaID)]
                Mtype = request.form['MediaType']
                update = values.SupdateMedia(MediaID, IdeaID, value, Mtype)
                if update:
                    flash('Edited successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem saving the Media! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            elif request.form['submit'] == 'delete':
                MediaID = request.form['id']
                IdeaID = request.form[str(MediaID)]
                delete = values.deleteMedia(MediaID, IdeaID)
                if delete:
                    flash('Media Deleted successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem deleting the Media! Please try again!', 'warning')
            elif request.form['submit'] == 'image':
                IdeaID = request.form['id']
                if values.NoIdea(IdeaID):
                    flash(
                        'No Such Idea exists, for which you are adding Media. Please try again!', 'warning')
                    return redirect('/super/' + tablename)
                image_link = None
                image_link = upload_img(request.files['file'])
                if image_link:
                    MediaID = values.getLatestMedia() + 1
                    example_img = values.insertMedia(
                        MediaID, IdeaID, image_link, 'image', session['userid'], datetime.now())
                    if example_img:
                        flash('Media Added successfully!', 'success')
                        return redirect('/super/' + tablename)
                flash(
                    'There was problem adding the Media! Please try again!', 'warning')
                return redirect('/super/' + tablename)

            elif request.form['submit'] == 'text':
                IdeaID = request.form['id']
                if values.NoIdea(IdeaID):
                    flash(
                        'No Such Idea exists, for which you are adding Media. Please try again!', 'warning')
                    return redirect('/super/' + tablename)
                example = request.form['example']
                MediaID = values.getLatestMedia() + 1
                example_text = values.insertMedia(
                    MediaID, IdeaID, example, 'text', session['userid'], datetime.now())
                if example_text:
                    flash('Media Added successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem adding the Media! Please try again!', 'warning')
                return redirect('/super/' + tablename)

            else:
                pass

        elif table == 'Country':
            if request.form['submit'] == 'edit':
                LangID = request.form['LangID']
                CountryID = request.form['id']
                value = request.form[str(CountryID)]
                update = values.updateCountry(LangID, CountryID, value)
                if update:
                    flash('Edited successfully!', 'success')
                    return redirect('/super/' + tablename)

            elif request.form['submit'] == 'delete':
                LangID = request.form['LangID']
                CountryID = request.form['id']
                if values.CheckCountry(CountryID):
                    flash(
                        "This Country Can't be deleted,since it has states", 'warning')
                    return redirect('/super/' + tablename)
                delete = values.deleteCountry(LangID, CountryID)
                if delete:
                    flash('Country Deleted successfully!', 'success')
                    return redirect('/super/' + tablename)
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
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem saving the translation! Please try again!', 'warning')
                return redirect('/super/' + tablename)

            elif request.form['submit'] == 'add':
                LangID = session['LanguageID']
                CountryID = values.getCountryID(LangID)+1
                name = request.form['name']
                insert = values.insertCountry(
                    LangID, CountryID, name, session['userid'])
                if insert:
                    flash('Country Added successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem adding the Country! Please try again!', 'warning')
                return redirect('/super/' + tablename)

        elif table == 'State':
            if request.form['submit'] == 'edit':
                LangID = request.form['LangID']
                CountryID = request.form['CountryID']
                StateID = request.form['StateID']
                value = request.form[str(StateID)]
                update = values.updateState(LangID, CountryID, StateID, value)
                if update:
                    flash('Edited successfully!', 'success')
                    return redirect('/super/' + tablename)

            elif request.form['submit'] == 'delete':
                LangID = request.form['LangID']
                CountryID = request.form['CountryID']
                StateID = request.form['StateID']
                if values.CheckState(StateID):
                    flash(
                        "This State Can't be deleted,since it has districts", 'warning')
                    return redirect('/super/' + tablename)
                delete = values.deleteState(LangID, CountryID, StateID)
                if delete:
                    flash('State Deleted successfully!', 'success')
                    return redirect('/super/' + tablename)
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
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem saving the translation! Please try again!', 'warning')
                return redirect('/super/' + tablename)

            elif request.form['submit'] == 'add':
                CountryID = request.form['CID']
                if values.NoCountry(CountryID):
                    flash(
                        'No Such Country exists, for which you are adding State. Please try again!', 'warning')
                    return redirect('/super/' + tablename)
                LangID = session['LanguageID']
                name = request.form['name']
                StateID = values.getStateID(LangID, CountryID) + 1
                insert = values.insertState(
                    LangID, CountryID, StateID, name, session['userid'])
                if insert:
                    flash('State Added successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem adding the State! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            else:
                pass

        elif table == 'District':
            if request.form['submit'] == 'edit':
                LangID = request.form['LangID']
                CountryID = request.form['CountryID']
                StateID = request.form['StateID']
                DistrictID = request.form['DistrictID']
                value = request.form[str(DistrictID)]
                update = values.updateDistrict(
                    LangID, CountryID, StateID, DistrictID, value)
                if update:
                    flash('Edited successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was an error while editing! Please try again!', 'danger')
            elif request.form['submit'] == 'delete':
                LangID = request.form['LangID']
                CountryID = request.form['CountryID']
                StateID = request.form['StateID']
                DistrictID = request.form['DistrictID']
                if values.CheckDistrict(DistrictID):
                    flash(
                        "This District Can't be deleted,since it has blocks", 'warning')
                    return redirect('/super/' + tablename)
                delete = values.deleteDistrict(
                    LangID, CountryID, StateID, DistrictID)
                if delete:
                    flash('District Deleted successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem deleting the District! Please try again!', 'warning')

            elif request.form['submit'] == 'add':
                CountryID = request.form['CID']
                if values.NoCountry(CountryID):
                    flash(
                        'No Such Country exists, for which you are adding State. Please try again!', 'warning')
                    return redirect('/super/' + tablename)
                StateID = request.form['SID']
                if values.NoState(StateID):
                    flash(
                        'No Such State exists, for which you are adding District. Please try again!', 'warning')
                    return redirect('/super/' + tablename)
                LangID = session['LanguageID']
                name = request.form['name']
                DistrictID = values.getDistrictID(
                    LangID, CountryID, StateID) + 1
                insert = values.insertDistrict(
                    LangID, CountryID, StateID, DistrictID, name, session['userid'])
                if insert:
                    flash('District Added successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem adding the District! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            else:
                pass

        elif table == 'Block':
            if request.form['submit'] == 'edit':
                LangID = request.form['LangID']
                CountryID = request.form['CountryID']
                StateID = request.form['StateID']
                DistrictID = request.form['DistrictID']
                BlockID = request.form['BlockID']
                value = request.form[str(BlockID)]
                update = values.updateDistrict(
                    LangID, CountryID, StateID, DistrictID, BlockID, value)
                if update:
                    flash('Block Edited successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was an error while editing! Please try again!', 'danger')
            elif request.form['submit'] == 'delete':
                LangID = request.form['LangID']
                CountryID = request.form['CountryID']
                StateID = request.form['StateID']
                DistrictID = request.form['DistrictID']
                BlockID = request.form['BlockID']
                delete = values.deleteBlock(
                    LangID, CountryID, StateID, DistrictID, BlockID)
                if delete:
                    flash('Block Deleted successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem deleting the Block! Please try again!', 'warning')

            elif request.form['submit'] == 'add':
                CountryID = request.form['CID']
                StateID = request.form['SID']
                DistrictID = request.form['DID']
                name = request.form['name']
                LangID = session['LanguageID']
                if values.NoCountry(CountryID):
                    flash(
                        'No Such Country exists, for which you are adding Block. Please try again!', 'warning')
                    return redirect('/super/' + tablename)
                if values.NoState(StateID):
                    flash(
                        'No Such State exists, for which you are adding Block. Please try again!', 'warning')
                    return redirect('/super/' + tablename)
                if values.NoDistrict(DistrictID):
                    flash(
                        'No Such District exists, for which you are adding Block. Please try again!', 'warning')
                    return redirect('/super/' + tablename)
                BlockID = values.getBlockID(
                    LangID, CountryID, StateID, DistrictID) + 1
                insert = values.insertBlock(
                    LangID, CountryID, StateID, DistrictID, BlockID, name, session['userid'])
                if insert:
                    flash('Block Added successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem adding the Block! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            else:
                pass

        elif table == 'Category':
            if request.form['submit'] == 'edit':
                LangID = request.form['LangID']
                CatID = request.form['id']
                value = request.form[str(CatID)]
                update = values.updateCat(LangID, CatID, value)
                if update:
                    flash('Edited successfully!', 'success')
                    return redirect('/super/' + tablename)
            elif request.form['submit'] == 'delete':
                LangID = request.form['LangID']
                CategoryID = request.form['id']
                if values.CheckCategory(CategoryID):
                    flash(
                        "This Category Can't be deleted, since it has subcategories", 'warning')
                    return redirect('/super/' + tablename)
                delete = values.deleteCategory(LangID, CategoryID)
                if delete:
                    flash('Category Deleted successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem deleting the Category! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            elif request.form['submit'] == 'translate':
                CatID = request.form['id']
                langid = request.form['language']
                value = request.form[str(CatID)+'translate']
                update = values.insertCat(
                    CatID, langid, value, session['userid'])
                if update:
                    flash('Translated successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem saving the translation! \
                    Please try again!', 'warning')
                return redirect('/super/' + tablename)
            elif request.form['submit'] == 'add':
                value = request.form['name']
                LangID = session['LanguageID']
                CatID = values.getCatID(LangID) + 1
                insert = values.insertCat(
                    CatID, LangID, value, session['userid'])
                if insert:
                    flash('Category Added successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem adding the Category! Please try again!',
                    'warning')
                return redirect('/super/' + tablename)
            else:
                pass
        elif table == "SubCategory":
            if request.form['submit'] == 'edit':
                LangID = request.form['LangID']
                CatID = request.form['CatID']
                SubCatID = request.form['SubCatID']
                value = request.form[str(SubCatID)]
                update = values.updateSubCat(LangID, CatID, SubCatID, value)
                if update:
                    flash('Edited successfully!', 'success')
                    return redirect('/super/' + tablename)
            elif request.form['submit'] == 'delete':
                LangID = request.form['LangID']
                CatID = request.form['CatID']
                SubCatID = request.form['SubCatID']
                delete = values.deleteSub(LangID, CatID, SubCatID)
                if delete:
                    flash('SubCategory Deleted successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem deleting the SubCategory! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            elif request.form['submit'] == 'translate':
                CatID = request.form['id']
                SubCatID = request.form['SubCatID']
                langid = request.form['language']
                value = request.form[str(SubCatID)+'translate']
                update = values.insertSubCat(
                    CatID, SubCatID, langid, value, session['userid'])
                if update:
                    flash('Translated successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem saving the translation! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            elif request.form['submit'] == 'add':
                CategoryID = request.form['CID']
                if values.NoCategory(CategoryID):
                    flash(
                        'No Such Category exists, for which you are adding SubCategory. Please try again!', 'warning')
                    return redirect('/super/' + tablename)
                LangID = session['LanguageID']
                name = request.form['name']
                SubCategoryID = values.getSubCatID(LangID, CategoryID) + 1
                insert = values.insertSubCat(
                    CategoryID, SubCategoryID, LangID, name, session['userid'])
                if insert:
                    flash('SubCategory Added successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem adding the SubCategory! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            else:
                pass
        elif table == 'Stage':
            if request.form['submit'] == 'edit':
                LangID = request.form['LangID']
                StageID = request.form['id']
                value = request.form[str(StageID)]
                update = values.updateStage(LangID, StageID, value)
                if update:
                    flash('Edited successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was editing the Stage! Please try again!',
                    'warning')
                return redirect('/super/' + tablename)
            elif request.form['submit'] == 'delete':
                LangID = request.form['LangID']
                StageID = request.form['id']
                delete = values.deleteStage(LangID, StageID)
                if delete:
                    flash('Stage Deleted successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem deleting the Stage! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            elif request.form['submit'] == 'add':
                value = request.form['name']
                LangID = session['LanguageID']
                StageID = values.getStageID(LangID) + 1
                insert = values.insertStage(
                    LangID, StageID, value, session['userid'])
                if insert:
                    flash('Stage Added successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem adding the Stage! Please try again!',
                    'warning')
                return redirect('/super/' + tablename)
            else:
                pass
        elif table == "Language":
            # Todo: test
            if request.form['submit'] == 'add':
                name = request.form['name']
                insert = values.insertLang(name, session['userid'])
                if insert:
                    flash('Language Added successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem adding the Language! Please try again!',
                    'warning')
                return redirect('/super/' + tablename)
            elif request.form['submit'] == 'edit':
                LangID = request.form['id']
                name = request.form[str(LangID)]
                masterlang = request.form['master']
                update = values.updateLang(LangID, name, masterlang)
                if update:
                    flash('Edited successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem editing the Language! Please try again!',
                    'warning')
                return redirect('/super/' + tablename)
            elif request.form['submit'] == 'delete':
                LangID = request.form['id']
                if values.checkLang(LangID):
                    flash(
                        "This Language Can't be deleted", 'warning')
                    return redirect('/super/' + tablename)
                delete = values.deleteLang(LangID)
                if delete:
                    flash('Language Deleted successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem deleting the Language! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            else:
                pass
        elif table == "Benefit":
            if request.form['submit'] == 'edit':
                LangID = request.form['LangID']
                BenefitID = request.form['id']
                value = request.form[str(BenefitID)]
                update = values.updateBenefit(LangID, BenefitID, value)
                if update:
                    flash('Edited successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was editing the Stage! Please try again!',
                    'warning')
                return redirect('/super/' + tablename)
            elif request.form['submit'] == 'delete':
                LangID = request.form['LangID']
                BenefitID = request.form['id']
                delete = values.deleteBenefit(LangID, BenefitID)
                if delete:
                    flash('Benefit Deleted successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem deleting the Benefit! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            elif request.form['submit'] == 'add':
                value = request.form['name']
                LangID = session['LanguageID']
                BenefitID = values.getBenefitID(LangID) + 1
                insert = values.insertBenefit(
                    LangID, BenefitID, value, session['userid'])
                if insert:
                    flash('Benefit Added successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem adding the Benefit! Please try again!',
                    'warning')
                return redirect('/super/' + tablename)
            else:
                pass
        elif table == "Menu":
            if request.form['submit'] == 'edit':
                LangID = request.form['LangID']
                MenuID = request.form['id']
                PageName = request.form['PageName']
                FormName = request.form[str(MenuID)]
                FormLink = request.form['FormLink']
                RoleID = request.form['Role']
                update = values.updateMenuForm(
                    LangID, MenuID, PageName, FormName, FormLink, RoleID)
                if update:
                    flash('Edited successfully!', 'success')
                flash(
                    'There was problem editing the Menu! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            elif request.form['submit'] == 'delete':
                LangID = request.form['LangID']
                MenuID = request.form['id']
                if values.CheckMenu(MenuID):
                    flash(
                        "This Menu Can't be deleted,since it has SubMenus", 'warning')
                    return redirect('/super/' + tablename)
                delete = values.deleteMenu(LangID, MenuID)
                if delete:
                    flash('Menu Deleted successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem deleting the Menu! Please try again!', 'warning')

            elif request.form['submit'] == 'add':
                LangID = session['LanguageID']
                PageName = request.form['PageName']
                FormName = request.form['name']
                FormLink = request.form['FormLink']
                RoleID = request.form['Role']
                MenuID = values.getMenuID(LangID)+1
                insert = values.insertMenu(
                    (LangID, MenuID, PageName, FormName, FormLink, RoleID, session['userid'], datetime.now()))
                if insert:
                    flash('Menu Added successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem adding the Menu! Please try again!', 'warning')
                return redirect('/super/' + tablename)
        elif table == "SubMenu":
            if request.form['submit'] == 'edit':
                LangID = request.form['LangID']
                MenuID = request.form['id']
                SubMenuID = request.form[str(MenuID)]
                FormName = request.form[str(SubMenuID)]
                FormLink = request.form['FormLink']
                RoleID = request.form['Role']
                update = values.updateSubMenuForm(
                    LangID, MenuID, SubMenuID, FormName, FormLink, RoleID)
                if update:
                    flash('Edited successfully!', 'success')
                flash(
                    'There was problem editing the SubMenu! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            elif request.form['submit'] == 'delete':
                LangID = request.form['LangID']
                MenuID = request.form['id']
                SubMenuID = request.form[str(MenuID)]
                delete = values.deleteSubMenu(LangID, MenuID, SubMenuID)
                if delete:
                    flash('SubMenu Deleted successfully!', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem deleting the SubMenu! Please try again!', 'warning')

            elif request.form['submit'] == 'add':
                LangID = session['LanguageID']
                MenuID = request.form['id']
                FormName = request.form['name']
                FormLink = request.form['FormLink']
                RoleID = request.form['Role']
                if values.NoMenu(LangID, MenuID):
                    flash(
                        'No Such Menu exists, for which you are adding SubMenu. Please try again!', 'warning')
                    return redirect('/super/' + tablename)
                SubMenuID = values.getSubMenuID(LangID, MenuID)+1
                insert = values.insertSubMenu(
                    (LangID, MenuID, SubMenuID, FormName, FormLink, RoleID, session['userid'], datetime.now()))
                if insert:
                    flash('SubMenu Added successfully!', 'success')
                flash(
                    'There was problem adding the SubMenu! Please try again!', 'warning')
                return redirect('/super/' + tablename)
        elif table == 'Registration':
            if request.form['submit'] == 'edit':
                cols = values.getColumns(table)
                details = []
                details.append(request.form['LoginID'])
                for count in range(1,len(cols)-2):
                    details.append(request.form[str(count)])
                updatevals = values.update_register(*details)
                if updatevals:
                    flash('Updated Registration Details.', 'success')
                flash(
                    'There was problem editing the Registration! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            elif request.form['submit'] == 'delete':
                LoginID = request.form['LoginID']
                if values.IdeaReg(LoginID):
                    flash(
                    'This Registration Cant be deleted since it has ideas!', 'danger')
                    return redirect('/super/' + tablename)
                delete = values.deleteReg(LoginID)
                if delete:
                    flash('Deleted Registration Details.', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem deleting the Registration! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            else:
                pass
        elif table == 'Idea':
            if request.form['submit'] == 'edit':
                cols = values.getColumns(table)
                details = []
                details.append(request.form['IdeaID'])
                for count in range(2,len(cols)-2):
                    details.append(request.form[str(count)])
                updatevals = values.updateIdea(*details)
                if updatevals:
                    flash('Updated Idea Details.', 'success')
                flash(
                    'There was problem editing the Idea! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            elif request.form['submit'] == 'delete':
                IdeaID = request.form['IdeaID']
                if values.checkIdeaentry(IdeaID):
                    flash(
                    'This Idea cant be deleted!', 'danger')
                    return redirect('/super/' + tablename)
                delete = values.deleteIdea(IdeaID)
                if delete:
                    flash('Deleted Idea Details.', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem deleting the Idea! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            else:
                pass
        elif table == 'IdeaCatSubCat':
            if request.form['submit'] == 'edit':
                cols = values.getColumns(table)
                details = []
                details.append(request.form['IdeaID'])
                details.append(request.form['CatID'])
                details.append(request.form['SubCatID'])
                for count in range(len(cols)-2):
                    details.append(request.form[str(count)])
                print(details)
                updatevals = values.updateICS(*details)
                if updatevals:
                    flash('Updated Idea and Category Details.', 'success')
                flash(
                    'There was problem editing the Idea and Category! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            elif request.form['submit'] == 'delete':
                details = []
                details.append(request.form['IdeaID'])
                details.append(request.form['CatID'])
                details.append(request.form['SubCatID'])
                delete = values.deleteICS(*details)
                if delete:
                    flash('Deleted Idea and Category Details.', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem deleting the Idea! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            else:
                pass
        elif table == 'Login':
            if request.form['submit'] == 'edit':
                cols = values.getColumns(table)
                details = []
                details.append(request.form['LoginID'])
                for count in range(1, len(cols)-2):
                    details.append(request.form[str(count)])
                updatevals = values.updateLogin(*details)
                if updatevals:
                    flash('Updated Login Details.', 'success')
                flash(
                    'There was problem editing the Login Details! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            elif request.form['submit'] == 'delete':
                if values.NoLogin(request.form['LoginID']):
                    flash(
                        'This Login Cant be deleted since it has Registration details!', 'danger')
                    return redirect('/super/' + tablename)
                delete = values.deleteLogin(request.form['LoginID'])
                if delete:
                    flash('Deleted Login Details.', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem deleting the Login! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            elif request.form['submit'] == 'add':
                LoginID = values.LoginID()+1
                Username = request.form['Username']
                Password = request.form['Password']
                RoleID = int(request.form['RoleID'])
                if RoleID == 2:
                    RoleName = 'dataentry'
                elif RoleID == 3:
                    RoleName = 'viewer'
                elif RoleID == 4:
                    RoleName = 'admin'
                elif RoleID == 5:
                    RoleName = 'superadmin'
                cr_by = session['userid']
                insert = values.createLogin(
                    LoginID, Username, Password, RoleID, RoleName, cr_by, datetime.now())
                if insert:
                    flash('Account Added successfully!', 'success')
                flash(
                    'There was problem adding the Account! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            else:
                pass
        elif table == 'Label':
            if request.form['submit'] == 'edit':
                details = []
                details.append(request.form['LabelID'])
                cols = values.getColumns(table)
                for count in range(1, len(cols)-2):
                    details.append(request.form[str(count)])
                updatevals = values.updateLabelSA(*details)
                if updatevals:
                    flash('Updated Label Details.', 'success')
                flash(
                    'There was problem editing the Label Details! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            elif request.form['submit'] == 'delete':
                delete = values.deleteLabel(request.form['LabelID'],request.form['1'])
                if delete:
                    flash('Deleted Label.', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem deleting the Label! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            elif request.form['submit'] == 'add':
                LanguageID = request.form['LanguageID']
                LabelID = values.getLabelID(LanguageID)+1
                RoleID = request.form['RoleID']
                PageName = request.form['PageName']
                LabelType = request.form['LabelType']
                LabelValue = request.form['LabelValue']
                cr_by = session['userid']
                cr_date = datetime.now()
                insert = values.insertLabel(
                    (LabelID, LanguageID, RoleID, PageName, LabelType, LabelValue, cr_by, cr_date))
                if insert:
                    flash('Added Label.', 'success')
                    return redirect('/super/' + tablename)
                flash(
                    'There was problem Adding a new Label! Please try again!', 'warning')
                return redirect('/super/' + tablename)
            else:
                pass
        else:
            pass


@app.route('/language/<int:langid>')
def language(langid):
    session.pop('LanguageID', None)
    session['LanguageID'] = langid
    return redirect(request.args.get('next') or url_for('index'))

if __name__ == '__main__':
    print "Fetching data..."
    # print os.path.dirname(os.path.abspath(__file__))
    languages = values.gettablevalues('Language')
    for lang in languages:
        if lang[2] == 1:
            masterlang = lang[0]
            break
    labels = values.gettablevalues('Label')
    menus = values.gettablevalues('Menu')
    submenus = values.gettablevalues('SubMenu')
    categories = values.gettablevalues('Category')
    subcategories = values.gettablevalues('SubCategory')
    country = values.gettablevalues('Country')
    state = values.gettablevalues('State')
    district = values.gettablevalues('District')
    block = values.gettablevalues('Block')
    benefits = values.gettablevalues('Benefit')
    stages = values.gettablevalues('Stage')
    category = values.gettablevalues('Category')
    subcat = values.gettablevalues('SubCategory')
    tables = values.gettablelist()
    ideas = values.gettablevalues('Idea')
    print "Data fetched successfully!"
    app.run(debug=True, host='0.0.0.0', port=3000)
