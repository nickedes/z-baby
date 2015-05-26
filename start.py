import os
from flask import (
                    Flask,
                    render_template,
                    session,
                    request
                )
from admin import adminobj
from teacher import teacherobj

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.register_blueprint(teacherobj, subdomain='teacher')
app.register_blueprint(adminobj, subdomain='admin')

from errors import showerrors
showerrors(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
        return "lolpol"


@app.route('/ziiei')
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
    return


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return "get page"
    elif request.method == 'POST':
        username = request.form.get('Username')
        #check is username exists
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
    app.run(debug=True)
