
def showerrors(app):
	@app.errorhandler(404)
	def page_not_found(error):
	    return error