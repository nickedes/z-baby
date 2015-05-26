from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about/')
@app.route('/about/<name>')
def about(name):
    if name == "ZIIEI":
        return render_template('ziiei.html')
    elif name == "Aurbindo":
        return render_template('aurbindo.html')
    elif name == "Litchi":
        return render_template('litchi.html')
    elif name == "UP Govt":
        return


@app.route('/ZIIEI/')
@app.route('/ZIIEI/<page>')
def ziiei(page):
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

@app.route('/login')
def login():
	return

@app.route('/faq')
def faq():
	return

@app.route('/contact-us')
def contact():
	return

if __name__ == '__main__':
    app.run(debug=True)
