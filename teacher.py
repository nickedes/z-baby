from flask import (
				Blueprint,
				request,
				session
				)


teacherobj = Blueprint('teacher', __name__)

@teacherobj.route('/')
def teacher():
	return None