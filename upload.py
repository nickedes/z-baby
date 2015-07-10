from values import getVimeo


def VideoUpload(video_path):
	video = getVimeo()
	video_uri = video.upload(video_path)
	return video_uri
