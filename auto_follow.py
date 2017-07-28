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
username = 'stratus009'
password = 'enter_saNdy3k'
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


userinfo = api.username_info('adilmahfud_')
userfollowers = api.user_followers(userinfo['user']['pk'])
# print json.dumps(userfollowers['users'], indent=4, sort_keys=True)
print len(userfollowers['users'])
users = userfollowers['users']
count = 0
for user in users:
    status = api.friendships_create(user['pk'])
    time.sleep(1)
    count = count+1
    print 'Followed username:', user['username']
    print count
    if count % 20 == 0:
        time.sleep(300)
print 'Total followed:', count