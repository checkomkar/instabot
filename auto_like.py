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
import random
username = 'stratus009'
password = 'enter_saNdy3k'
myId = '19335645'
settings_file = './settings.json'
comments = ['Wow! O.O (y)', 'Very Nice :) love it', 'Awesome! Keep em coming!', 'Just Love it!', 'Super like! O.o']
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


# userinfo = api.user_detail_info('vijay_jangid_sunil')
nxtPageId = None
catchedMediaIds = None
mediaIdsArray = []
useridinfo = api.explore()
nxtPageId = useridinfo['next_max_id']


nextPage = api.explore(max_id = useridinfo['next_max_id'])

# print json.dumps(useridinfo, indent=4, sort_keys=True)
print 'Next page'
# print json.dumps(nextPage, indent=4, sort_keys=True)
for media in useridinfo['items']:
    if 'media' in media:
        if media['media']['caption'] is not None:
            if 'media_id' in media['media']['caption']:
                # print json.dumps(media['media']['caption']['media_id'], indent=4, sort_keys=True)
                mediaIdsArray.append(media['media']['caption']['media_id'])

itercount = 1
for _ in itertools.repeat(None, 20):    
    nextPage = api.explore(max_id = itercount)
    for media in nextPage['items']:
        if 'media' in media:
            if media['media']['caption'] is not None:
                if 'media_id' in media['media']['caption']:
                    # print json.dumps(media['media']['caption']['media_id'], indent=4, sort_keys=True)
                    mediaIdsArray.append(media['media']['caption']['media_id'])
    itercount = itercount+1

print 'Array Length:', len(mediaIdsArray)
print map(str, mediaIdsArray)

likecount = 0
for count, m_id in enumerate(mediaIdsArray, 1):
    print 'Media:', m_id
    status = api.post_like(m_id)
    time.sleep(4)

    if status['status'] == 'ok':
        likecount = likecount + 1

    if count % 5 == 0:
        commentStatus = api.post_comment(m_id, random.choice(comments))
        print json.dumps(commentStatus, indent=4, sort_keys=True)
        
    print json.dumps(status, indent=4, sort_keys=True)
    print likecount

# info = api.media_info('1535747968551861555')
# print json.dumps(info, indent=4, sort_keys=True)
    # if key == 'media':
    #     print media['media']['caption']['media_id']


# getSearchFeed = api.feed_tag('mountains')
# maxidFeed = None

# # print json.dumps(getSearchFeed['ranked_items'][0]['caption']['media_id'], indent=4, sort_keys=True)

# for media in getSearchFeed['ranked_items']:
#     print json.dumps(media['caption']['media_id'], indent=4, sort_keys=True)
#     maxidFeed = media['next_max_id']

# getNxtSrchFeed = api.feed_tag('mountains', max_id= maxidFeed)
# print json.dumps(getNxtSrchFeed, indent=4, sort_keys=True)
# for media in getNxtSrchFeed:
#     print json.dumps(media, indent=4, sort_keys=True)
# with open('dump.json', 'w') as outfile:
#     json.dump(getSearchFeed, outfile)
# commentPost = api.post_comment('1534294934576111156', 'Great View')
# print json.dumps(commentPost, indent=4, sort_keys=True)
# mediaLiked = api.post_like('1534294934576111156')
# print json.dumps(mediaLiked, indent=4, sort_keys=True)