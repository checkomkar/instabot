import web
import datetime

from cachedSettings import *
api = run_cached()
today = datetime.date.today()
f = open('log.txt', 'a')



class autoFollow:
	def GET(self):
		username_local = web.input(name='fender')
		userinfo = api.username_info(username_local.name)
		userfollowers = api.user_followers(userinfo['user']['pk'])
		users = userfollowers['users']
		count = 0
		response = []
		usersFollowed = []
		f.write('starting to follow... \n')
		for user in users:
			userInfo = {}
			status = api.friendships_create(user['pk'])
			time.sleep(4)
			count = count+1
			f.write(user['username']) 
			userInfo['info'] = user.copy()
			userInfo['status'] = status
			usersFollowed.append(userInfo.copy())
			# f.write(count)
			if count % 20 == 0:
				time.sleep(300)
		# f.write(count) 
		response.append(count)
		response.append(usersFollowed)
		f.close()
		return json.dumps(response, indent=4, sort_keys=True)