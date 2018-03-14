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
import logging
import socket
import sys


lock_socket = None  # we want to keep the socket open until the very end of
                    # our script so we use a global variable to avoid going
                    # out of scope and being garbage-collected

def is_lock_free():
    global lock_socket
    lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        lock_id = "checkomkar.autoliketags"   # this should be unique. using your username as a prefix is a convention
        lock_socket.bind('\0' + lock_id)
        logging.debug("Acquired lock %r" % (lock_id,))
        return True
    except socket.error:
        # socket already locked, task must already be running
        logging.info("Failed to acquire lock %r" % (lock_id,))
        return False

if not is_lock_free():
    sys.exit()




username = 'stra.tus'
password = 'enter_sandmany3k'
myId = '19335645'
settings_file = './settings.json'
# settings_file = '/home/checkomkar/instabot/settings.json'

tags = ["nature", "bitemykitchen", "PleaseForgiveMe", "sky", "sun", "summer", "beach", "beautiful", 
            "pretty", "sunset", "sunrise", "blue", "flowers", "night", "tree", "twilight", "clouds", 
            "beauty", "light", "cloudporn", "photooftheday", "love", "green", "skylovers", "dusk", "weather", 
            "day", "red", "mothernature", "models", "babes", "sexy", "travel", 
            "travelphotography", "travelchannel", "travelandleisure", "tagblender", 
            "picoftheday", "tbt", "picpets", "vida", "pets", "nature", "me", "awesome_shots", 
            "nature_shooters", "cute", "instagood", "love", "kittensofinstagram", "love", 
            "sweet", "tweegram", 
            "photooftheday", "animales", "catsofinstagram", "animals", "instamood", "iphonesia", "fauna"]
comments = ['Wow! O.O (y)', 'Such splendid.', 'Overly alluring shot =)', 
            'This is revolutionary work =)', 'Incredible work you have here.', 'Very Nice :) love it', 
            'Awesome! Keep em coming!', 'Magnificent. So amazing.', 'Just cool!', 'Cool shot.',
            'It\'s excellent not just good!', 
            'Just Love it!', 'Super like! O.o']
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


def auto_like_tags(isliked = False):
    nxtPageId = None
    catchedMediaIds = None
    mediadict = {}
    mediaIdsArray = []
    random.shuffle(tags)
    for tag in tags:
        print 'Tag:', tag
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
            likers = api.media_likers(m_id['id'])
            # print json.dumps(likers, indent=4, sort_keys=True)
            for liker in likers['users']:
                # print 'Liker: ', json.dumps(liker, indent=4, sort_keys=True)
                if liker['username'] == 'stra.tus':
                    isliked = True
                    break
            
            if isliked == False and count % 5 == 0:  
                commentStatus = api.post_comment(m_id['id'], random.choice(comments))
                print json.dumps(commentStatus, indent=4, sort_keys=True) 
                # print random.choice(comments)                
                time.sleep(20)
            
            isliked = False 
            status = api.post_like(m_id['id'])

            if status['status'] == 'ok':
                likecount = likecount + 1
                # minfo = api.media_comments(m_id['id'])
                # print json.dumps(minfo, indent=4, sort_keys=True)

            
            print json.dumps(status, indent=4, sort_keys=True)
            print likecount
            if likecount % 50 == 0:
                time.sleep(200)
            time.sleep(10)

# auto_like_tags(isliked = False)
    
def queryRepeatedly():
    while True:
        try:
            auto_like_tags(isliked = False)
        except:
            continue
        time.sleep(300)

queryRepeatedly()
