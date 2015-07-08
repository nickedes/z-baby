from vimeo import VimeoClient
from values import getVimeo


def upload(video_path):
	video = getVimeo()
	video_uri = video.upload(video_path)
	return video_uri
