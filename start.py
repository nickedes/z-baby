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
vals1 = {}
vals2 = []
vals3 = []
vals4 = []

app = Flask(__name__)
app.secret_key = os.urandom(24)

showerrors(app)


@app.route('/')
def index():
    session['Language'] = 1
    global vals1
    global vals2
    global vals3
    global vals4
    vals1, vals2, vals3, vals4 = values.retrieveValues(session['Language'])
    return render_template('index.html', labels=vals1, menu=vals2,
                           submenu=vals3, menulist=vals4)


@app.route('/about')
def about():
    return render_template('index.html')


@app.route('/ziiei/<page>')
def ziiei(page="workflow"):
    if page == "workflow":
        return
    elif page == "apply":
        return
    elif page == "benefits":
        return
    elif page == "examples":
        return
    elif page == "terms":
        return


@app.route('/register')
def register():
    session['Language'] = 1
    register_labels, register_sublabels = values.getRegisteration_Labels(
        session['Language'])
    return render_template('register.html', register_labels=register_labels,
                           register_sublabels=register_sublabels, labels=vals1,
                           menu=vals2, submenu=vals3, menulist=vals4)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('signin.html', labels=vals1,
                               menu=vals2, submenu=vals3, menulist=vals4)
    elif request.method == 'POST':
        username = request.form.get('Username')
        # check if username exists
        session["username"] = username


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/faq')
def faq():
    return


@app.route('/contact')
def contact():
    return

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
