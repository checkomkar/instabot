import datetime
import logging
import random

tags = ['travelstagram']
comments = ['Wow! O.O (y)', 'Very Nice :) love it', 'Awesome! Keep em coming!', 'Just Love it!', 'Super like! O.o']


def auto_like():
	nxtPageId = None
	catchedMediaIds = None
	mediadict = {}
	mediaIdsArray = []
	response = []
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

		for _ in itertools.repeat(None, 1):
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
			item = {}
			print 'Media:', m_id
			status = api.post_like(m_id['id'])
			item['like_status'] = status
			time.sleep(4)

			if status['status'] == 'ok':
				likecount = likecount + 1
				minfo = api.media_comments(m_id['id'])					
				print json.dumps(minfo, indent=4, sort_keys=True)

			if count % 5 == 0:
				commentStatus = api.post_comment(m_id['id'], random.choice(comments))
				item['comment_status'] = commentStatus
				print json.dumps(commentStatus, indent=4, sort_keys=True)
			    
			print json.dumps(status, indent=4, sort_keys=True)
			print likecount
			response.append({'likecount': likecount})
			response.append(item)
	
	return json.dumps(response, indent=4, sort_keys=True)