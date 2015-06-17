# Z-baby
NOTE:

Development has shifted to windows (server reasons), but we think most of the original instructions should still work. Just replace pymssql with pyodbc, and enjoy the MASSIVE data fetch gains. (We actually changed due to some problems with pymssql's compatibility with hindi on windows, but pyodbc is blazing fast compared to pymssql. Like at least 100x)
Oh, and we also switched to python 2.7. Only change in the code is the print statements, though, so that's cool.

For setup on windows:

0. Clone the repo: `git clone https://github.com/nickedes/z-baby`
1. Make a virtualenv `virtualenv --python=python2.7 yourEnv`
2. Install all dependencies `pip install flask pyimgur pyodbc` (and anything else it asks, though I think this is it.)
3. ` python start.py `

ALSO, there's no config file (obviously). I would love to give you the config file, but the DB isn't mine :-\
Basically keep running step 3 and fixing errors till the errors stop popping up. Pretty simple, really.

Original Instructions: 

ZIIEI 

For Setup On linux:

1. Install virtualenv by `sudo pip install virtualenv`
2. Make a virtualenv `virtualenv --python=python2.7 yourEnv`
3. Activate your virtualenv `source yourEnv/bin/activate`
4. Install flask `pip install flask`
5. sudo apt-get install freetds-dev
6. pip install pymssql
7. Clone the repo: `git clone https://github.com/nickedes/z-baby`
8. `cd z-baby`
9. Run by `python start.py` 

Environment :

* Python 2.7
* Flask
* [Bootstrap](http://getbootstrap.com/)
