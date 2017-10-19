# Z-baby
NOTE: *This Works on Windows as well as Linux.*

For Setup On **Linux**:

1. Install virtualenv by `sudo pip install virtualenv`
2. Make a virtualenv `virtualenv --python=python2.7 yourEnv`
3. Activate your virtualenv `source yourEnv/bin/activate`
4. Clone the repo: `git clone https://github.com/nickedes/z-baby`
5. Now install the database connector, follow [these](http://lbolla.info/blog/2013/08/28/python-and-odbc).
6. Finally,
```
cd z-baby
pip install -r requirements.txt
python start.py
```

For setup on **Windows**:

1. Make a virtualenv `virtualenv --python=python2.7 yourEnv`
2. Activate Environment: 
```
    cd yourEnv
    Scripts\activate
    cd z-baby
```
3. Clone the repo: `git clone https://github.com/nickedes/z-baby`
4. Install all dependencies `pip install -r requirements.txt`
5. Run Project: `python start.py`

ALSO, there's no config file (obviously). I would love to give you the config file, but the DB isn't mine :wink:


Environment :

* Python 2.7
* Flask
* [Bootstrap](http://getbootstrap.com/)
