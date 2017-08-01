import web
from cachedSettings import *

api = run_cached()


urls = (
    '/', 'index',
    '/get-user-info', 'getUserInfo',
    '/get-info-post', 'getInfoPost',
    '/auto-like-comment', 'autoLikeComment',
    '/auto-follow', 'autoFollow'
)

class index:
    def GET(self):
    	info = api.username_info(username)        
        return json.dumps(info, indent=4, sort_keys=True)

class getUserInfo:
    def GET(self):
    	username_local = web.input(name='stratus009')
    	info = api.username_info(username_local.name)        
        return json.dumps(info, indent=4, sort_keys=True)

class getInfoPost:
    def POST(self):
    	data = web.data()
    	# info = api.username_info(username_local.name)        
        return data

from auto_follow_api import autoFollow
from auto_like_api import autoLikeComment

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()