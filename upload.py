from vimeo import VimeoClient

def conn():
	token = 'token'
	secret= 'secret'
	Client_Identifier= 'Client_Identifier'
	v = VimeoClient(
		token=token,
		key=Client_Identifier,
	    secret=secret)
	return v

def upload():
	video = conn()
	video_uri = video.upload('ytvid.MP4')
	print video_uri

upload()