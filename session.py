from instagram_private_api import (Client, ClientCompatPatch, ClientError, ClientLoginError, 
									ClientCookieExpiredError, 
									ClientLoginRequiredError, __version__ as client_version)
import json
import codecs
import time
import datetime
import os.path
import logging
import argparse
import itertools
username = 'stra.tus'
password = 'enter_sandy3K'
cookie = {"phone_model": "herolte", "created_ts": 1496078756, "app_version": "10.16.0", "ad_id": "ffbec3a7-44f9-4c96-77fb-3f597bb394e1", "uuid": "df3eb700-4493-11e7-b140-408d5cd81b95", "android_release": "6.0.1", "signature_key": "234623953a1374bd664075f5cfe54e642901db7acb778231f17e658300ea7934", "phone_device": "SM-G930F", "android_version": 23, "cookie": "(dp1\nS'i.instagram.com'\np2\n(dp3\nS'/'\n(dp4\nS'ds_user'\np5\n(icookielib\nCookie\np6\n(dp7\nS'comment'\np8\nNsS'domain'\np9\nS'i.instagram.com'\np10\nsS'name'\np11\ng5\nsS'domain_initial_dot'\np12\nI00\nsS'expires'\np13\nI1503854756\nsS'value'\np14\nS'stratus009'\np15\nsS'domain_specified'\np16\nI00\nsS'_rest'\np17\n(dp18\nsS'version'\np19\nI0\nsS'port_specified'\np20\nI00\nsS'rfc2109'\np21\nI00\nsS'discard'\np22\nI00\nsS'path_specified'\np23\nI01\nsS'path'\np24\nS'/'\nsS'port'\np25\nNsS'comment_url'\np26\nNsS'secure'\np27\nI00\nsbsS'mid'\np28\n(icookielib\nCookie\np29\n(dp30\ng8\nNsg9\nS'i.instagram.com'\np31\nsg11\ng28\nsg12\nI00\nsg13\nI2126798756\nsg14\nS'WSxZpAABAAG2bl1mXduXEFF3Ct4I'\np32\nsg16\nI00\nsg17\n(dp33\nsg19\nI0\nsg20\nI00\nsg21\nI00\nsg22\nI00\nsg23\nI01\nsg24\nS'/'\nsg25\nNsg26\nNsg27\nI00\nsbsS'ds_user_id'\np34\n(icookielib\nCookie\np35\n(dp36\ng8\nNsg9\nS'i.instagram.com'\np37\nsg11\ng34\nsg12\nI00\nsg13\nI1503854756\nsg14\nS'19335645'\np38\nsg16\nI00\nsg17\n(dp39\nsg19\nI0\nsg20\nI00\nsg21\nI00\nsg22\nI00\nsg23\nI01\nsg24\nS'/'\nsg25\nNsg26\nNsg27\nI00\nsbsS'csrftoken'\np40\n(icookielib\nCookie\np41\n(dp42\ng8\nNsg9\nS'i.instagram.com'\np43\nsg11\nS'csrftoken'\np44\nsg12\nI00\nsg13\nI1527528356\nsg14\nS'wXjuI6fDfn0LYuMq8ILcwl1cPuYfDwxB'\np45\nsg16\nI00\nsg17\n(dp46\nsg19\nI0\nsg20\nI00\nsg21\nI00\nsg22\nI00\nsg23\nI01\nsg24\nS'/'\nsg25\nNsg26\nNsg27\nI01\nsbsS'sessionid'\np47\n(icookielib\nCookie\np48\n(dp49\ng8\nNsg9\nS'i.instagram.com'\np50\nsg11\ng47\nsg12\nI00\nsg13\nI1503854756\nsg14\nS'IGSC200debe92f20a29e2d18e30bf92041bb84975510b8c4000a73fcdb728222302f%3A7TCNMHD92z6kVY0jLtzrbBAyprxDcPvn%3A%7B%22_auth_user_id%22%3A19335645%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_auth_user_hash%22%3A%22%22%2C%22_token_ver%22%3A2%2C%22_token%22%3A%2219335645%3AI5DJeu28r8H6Y6DTrOnqsrhUO8nypzbX%3A3f243238bbac6be4c6e8efef2b08022879dea727e5b6503ba91284d89ad5fa2b%22%2C%22_platform%22%3A1%2C%22asns%22%3A%7B%22time%22%3A1496078757%7D%2C%22last_refreshed%22%3A1496078757.0394048691%7D'\np51\nsg16\nI00\nsg17\n(dp52\nS'HttpOnly'\np53\nNssg19\nI0\nsg20\nI00\nsg21\nI00\nsg22\nI00\nsg23\nI01\nsg24\nS'/'\nsg25\nNsg26\nNsg27\nI01\nsbsS'rur'\np54\n(icookielib\nCookie\np55\n(dp56\ng8\nNsg9\nS'i.instagram.com'\np57\nsg11\nS'rur'\np58\nsg12\nI00\nsg13\nNsg14\nS'ATN'\np59\nsg16\nI00\nsg17\n(dp60\nsg19\nI0\nsg20\nI00\nsg21\nI00\nsg22\nI01\nsg23\nI01\nsg24\nS'/'\nsg25\nNsg26\nNsg27\nI00\nsbsss.", "phone_dpi": "640dpi", "phone_manufacturer": "samsung", "phone_resolution": "1440x2560", "key_version": "4", "phone_chipset": "samsungexynos8890", "ig_capabilities": "3boBAA==", "device_id": "android-df3eb701449311e7"}
myId = '19335645'
settings_file = './settings.json'
# myId = '25025320'
# with open('settings.json', 'r') as myfile:
#     data=myfile.read().replace('\n', '')

def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object

#use cached settings
try:

    if not os.path.isfile(settings_file):
        # settings file does not exist
        print('Unable to find file: {0!s}'.format(settings_file))

        # login new
        api = Client(
            username, password,
            on_login=lambda x: onlogin_callback(x, settings_file))
    else:
        with open(settings_file) as file_data:
            cached_settings = json.load(file_data, object_hook=from_json)
        print('Reusing settings: {0!s}'.format(settings_file))

        # device_id = cached_settings.get('device_id')
        # reuse auth settings
        api = Client(
            username, password,
            settings=cached_settings)
except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
        print('ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))
# with open(settings_file) as file_data:
#     cached_settings = json.load(file_data, object_hook=from_json)
# print('Reusing settings: {0!s}'.format(settings_file))
# api = Client(user_name, password, settings=cached_settings)
# results = api.feed_timeline()
#results = api.user_info('1570704704')
nxtId = None
reps = 0
for _ in itertools.repeat(None, 10):
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
	
	usersArr = []
	count = 0
	for user in results['users']:
		#print user['pk']
		usersArr.append(user['pk'])
		userFrndStatus = api.friendships_show(user['pk'])
		if userFrndStatus['followed_by'] == False:
			frndStatus = api.friendships_destroy(user['pk'])
			count = count+1
			print json.dumps(frndStatus, indent=4, sort_keys=True)
			print count
	print 'Total unfollows:', count

	while count == 0:
		if 'next_max_id' in nextResults:
			nextResults = api.user_following(myId, max_id=nextResults['next_max_id'])
		else:
			nextResults = api.user_following(myId)

		for user in nextResults['users']:
			#print user['pk']
			usersArr.append(user['pk'])
			userFrndStatus = api.friendships_show(user['pk'])
			if userFrndStatus['followed_by'] == False:
				frndStatus = api.friendships_destroy(user['pk'])
				count = count+1
				print json.dumps(frndStatus, indent=4, sort_keys=True)
		print 'Total unfollows:', count
	print 'End while'
	# showStatus = json.dumps(api.friendships_show(user['pk']), indent=4, sort_keys=True)
	# print showStatus
#print usersArr
# whois = api.user_info('437272073')
# print whois
# str1 = ''.join(str(e) for e in usersArr)
# showStatus = api.friendships_show_many(str1)
#for u in usersArr:

	#isFollowedBack = 


#print results['users'].length
#parsed = json.dumps(results['users'], indent=4, sort_keys=True)
#print parsed
#print(results)
# for item in items:
#     # Manually patch the entity to match the public api as closely as possible, optional
#     # To automatically patch entities, initialise the Client with auto_patch=True
#     ClientCompatPatch.media(item)
#     print(media['code'])