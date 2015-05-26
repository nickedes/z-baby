from flask import (
    Blueprint,
    request,
    session
)


teacherobj = Blueprint('teacher', __name__)


@teacherobj.route('/')
def teacher():
    return None


@teacherobj.route('/view')
def view():
    # View submitted ideas
    return None


@teacherobj.route('/insert')
def insert():
    return None


@teacherobj.route('/edit')
def edit():
    return None
