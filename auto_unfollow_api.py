import web
import datetime

from cachedSettings import *
api = run_cached()
myId = '19335645'

class autoUnfollow:
	def GET(self):
		nxtId = None
		reps = 0
		number = web.input(n=1)
		response = {}
		users_followed = []
		for _ in itertools.repeat(None, int(number.n)):
			reps = reps+1
			print 'repeating', reps
			results = api.user_following(myId)
			# items = results.get('items', [])
			#results = results.users
			#users = results['users']
			if 'next_max_id' in results:
				nxtId = results['next_max_id']
				nextResults = api.user_following(myId, max_id=nxtId)
			# print json.dumps(results, indent=4, sort_keys=True)
			# print json.dumps(nextResults, indent=4, sort_keys=True)
			# print json.dumps(results, indent=4, sort_keys=True)
			print len(results['users'])
			response['user_length'] = len(results['users'])
			usersArr = []
			count = 0

			for user in results['users']:
				#print user['pk']
				user_follow_status = {}
				usersArr.append(user['pk'])
				userFrndStatus = api.friendships_show(user['pk'])
				if userFrndStatus['followed_by'] == False:
					frndStatus = api.friendships_destroy(user['pk'])
					count = count+1
					print json.dumps(frndStatus, indent=4, sort_keys=True)
					user_follow_status['status'] = frndStatus
					user_follow_status['count'] = count
					user_follow_status['u_name'] = user['username']
					print count
					users_followed.append(user_follow_status)
			print 'Total unfollows:', count

			while count == 0:
				if 'next_max_id' in nextResults:
					nextResults = api.user_following(myId, max_id=nextResults['next_max_id'])
				else:
					nextResults = api.user_following(myId)

				for user in nextResults['users']:
					user_follow_status = {}
					#print user['pk']
					usersArr.append(user['pk'])
					userFrndStatus = api.friendships_show(user['pk'])
					if userFrndStatus['followed_by'] == False:
						frndStatus = api.friendships_destroy(user['pk'])
						count = count+1
						print json.dumps(frndStatus, indent=4, sort_keys=True)
						user_follow_status['status'] = frndStatus
						user_follow_status['count'] = count
						user_follow_status['u_name'] = user['username']
						users_followed.append(user_follow_status)
				print 'Total unfollows:', count
				
			print 'End while'
			response['user_length'] = len(api.user_following(myId))
			response['users_followed'] = users_followed
		return json.dumps(response, indent=4, sort_keys=True)
