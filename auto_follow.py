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
import pickle
from random import randint

username = 'stra.tus'
password = 'enter_sandmany3k'
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


users = ['eyebrows_tutorial', 'makeupgoals', 'eyelinertutorial', 'adilmahfud_', 'thehughjackman', 'tomcruise']

follows = []
count = 0
for user in users:    
    userinfo = api.username_info(user)
    userfollowers = api.user_followers(userinfo['user']['pk'])
    # print json.dumps(userfollowers['users'], indent=4, sort_keys=True)
    for idx, u in enumerate(userfollowers['users']):
        follows.append(u['pk'])
        
        # print u['pk']
    print len(userfollowers['users'])
    '''users = userfollowers['users']
    count = 0
    for user in users:
        status = api.friendships_create(user['pk'])
        time.sleep(1)
        count = count+1
        print 'Followed username:', user['username']
        print count
        if count % 20 == 0:
            time.sleep(300)
    print 'Total followed:', count'''

for idx, u in enumerate(follows):
    status = api.friendships_create(u)
    print json.dumps(status, indent=4, sort_keys=True)
    time.sleep(randint(5, 9))
    count = count+1
    # print 'Followed username:', u['username']
    print count
    if count % 20 == 0:
        time.sleep(300)
    if idx+1 % 160 == 0:
        time.sleep(60*60)

with open('follows.json', 'wb') as fp:
    pickle.dump(follows, fp)

with open ('follows.json', 'rb') as fp:
    itemlist = pickle.load(fp)
# print itemlist