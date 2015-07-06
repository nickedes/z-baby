import requests

def sendPassword():
	url = 'http://174.143.34.193/MtSendSMS/bulkSMS.aspx'
	usr = 'litchi'
	passwd = 'ign@sms'
	# &pass=
	# &msisdn=
	# &msg=nikhil,here%20:P
	# &sid=
	# &mt=4
	r = requests.post(url=url, data={'usr': usr,'pass':passwd,'msisdn':'9818993299',
		'msg':'heyy','sid':'LITCHI','mt':4})
	print r

sendPassword()