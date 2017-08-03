import web
from cachedSettings import *
from pprint import pprint

api = run_cached()


urls = (
    '/', 'index',
    '/get-user-info', 'getUserInfo',
    '/get-info-post', 'getInfoPost',
    '/auto-like-comment', 'autoLikeComment',
    '/auto-follow', 'autoFollow',
    '/auto-unfollow', 'autoUnfollow'
)

class index:
    def GET(self):
    	info = api.username_info(username)
        # info['web-context'] = json.dumps(web.ctx.home, indent=4, sort_keys=True)       
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
from auto_unfollow_api import autoUnfollow

if __name__ == "__main__":
    app = web.application(urls, globals())    
    # pprint(web.ctx)
    # if web.ctx.home == 'http://localhost:8080':
    #     app.run()
    # else:
    #     app = app.wsgifunc()
    # app.run()
    app = app.wsgifunc()