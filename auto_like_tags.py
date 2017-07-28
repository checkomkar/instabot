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
tags = ['travelstagram', 'travelphotography', 'photography', 'summer', 'summerbody',  'instagood', 'babesofinstagram']
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


nxtPageId = None
catchedMediaIds = None
mediadict = {}
mediaIdsArray = []

for tag in tags:
    searchFeeds = api.feed_tag(tag)
    nextmaxId = searchFeeds['next_max_id']

    for media in searchFeeds['items']:    
        if media['caption'] is not None:
            if 'media_id' in media['caption']:
                # print json.dumps(media['media']['caption']['media_id'], indent=4, sort_keys=True)
                mediadict['code'] = media['code']
                mediadict['id'] = media['caption']['media_id']
                mediaIdsArray.append(mediadict.copy())

    for media in searchFeeds['ranked_items']:    
        if media['caption'] is not None:
            if 'media_id' in media['caption']:
                # print json.dumps(media['media']['caption']['media_id'], indent=4, sort_keys=True)
                mediadict['code'] = media['code']
                mediadict['id'] = media['caption']['media_id']
                mediaIdsArray.append(mediadict.copy())
    # with open("dump.json", "w") as json_file:
    #     json.dump(mediaIdsArray, json_file)

    for _ in itertools.repeat(None, 20):
        searchFeeds = api.feed_tag(tag, max_id = nextmaxId)
        nextmaxId = searchFeeds['next_max_id']
        for media in searchFeeds['items']:    
            if media['caption'] is not None:
                if 'media_id' in media['caption']:
                    # print json.dumps(media['media']['caption']['media_id'], indent=4, sort_keys=True)
                    mediadict['code'] = media['code']
                    mediadict['id'] = media['caption']['media_id']
                    mediaIdsArray.append(mediadict.copy())
    # with open("dump.json", "w") as json_file:
    #     json.dump(mediaIdsArray, json_file)   

    print 'Array Length:', len(mediaIdsArray)
    # print map(str, mediaIdsArray)

    likecount = 0
    for count, m_id in enumerate(mediaIdsArray, 1):
        print 'Media:', m_id
        status = api.post_like(m_id['id'])
        time.sleep(4)

        if status['status'] == 'ok':
            likecount = likecount + 1
            minfo = api.media_comments(m_id['id'])
            print json.dumps(minfo, indent=4, sort_keys=True)

        if count % 5 == 0:
            commentStatus = api.post_comment(m_id['id'], random.choice(comments))
            print json.dumps(commentStatus, indent=4, sort_keys=True)
            
        print json.dumps(status, indent=4, sort_keys=True)
        print likecount


    
