from config import ACCESS_TOKEN, TT_MAIN
import requests
import json
import os.path

#This is the common prefix for all calls
GRAPH_URL_PREFIX = 'https://graph.facebook.com/'
#All data resulting from this code will be saved at this link:
SAVE_PATH='D:\Dropbox\Dropbox\Programming\Trainer_Tribe_Data'

#This is the limit on number of days and posts for which data will be extracted
FEED_LIMIT= 500
#DAYS= 

POST_EDGES= ['attachments','comments', 'likes', 'reactions']
#These conjunctions

FIELDS_CONJ = '?fields='
LIMITS_EDGE_CONJ = '?limit='
LIMITS_CONJ='.limit=('+str(FEED_LIMIT)+')'
SUMMARY_REQUEST='?summary=true'


COMMUNITY_FIELDS='groups'

GROUPS_SUFFIX = '/groups'
GROUP_FIELDS = 'id,name,members,privacy,description,updated_time'

MEMBERS_SUFFIX = '/members'
MEMBER_FIELDS = 'email,id,administrator,name'

FEED_SUFFIX= '/feed'
FEED_FIELDS='id,created_time,updated_time,from,message'
#Adjust how many results you want to stay visible


POST_FIELDS= 'id,created_time,updated_time,from,message'

JSON_KEY_DATA = 'data'
JSON_KEY_PAGING = 'paging'
JSON_KEY_NEXT = 'next'
JSON_KEY_EMAIL = 'email'


def getGroupMembers(access_token, group_id):
    endpoint = GRAPH_URL_PREFIX + group_id + MEMBERS_SUFFIX + FIELDS_CONJ + MEMBER_FIELDS
    return getPagedData(access_token, endpoint, [])

def getPostFields(access_token, post_id):
    endpoint= GRAPH_URL_PREFIX + post_id+ FIELDS_CONJ+ POST_FIELDS
    print(endpoint)
    return getJsonData(access_token, endpoint)

def getPostSummary(access_token, post_id, summary_type):
    endpoint= GRAPH_URL_PREFIX + post_id +"/" +summary_type +SUMMARY_REQUEST
    print(endpoint)
    return getJsonData(access_token, endpoint)

def getCommunityNumber(access_token):
    endpoint= GRAPH_URL_PREFIX+'community'
    return getJsonData(access_token, endpoint)

def getCommunityGroups(access_token, community_ID):
    endpoint= GRAPH_URL_PREFIX +community_ID+ FIELDS_CONJ + COMMUNITY_FIELDS
    print(endpoint)
    return getJsonData(access_token, endpoint)

def getLimitedGroupFeed(access_token, group_id):
    endpoint = GRAPH_URL_PREFIX + group_id + FIELDS_CONJ+'feed'+ LIMITS_CONJ 
    print(endpoint)
    return getJsonData(access_token, endpoint)

def getPagedData(access_token, endpoint, data):
    headers = buildHeader(access_token)
    result = requests.get(endpoint,headers=headers)
    result_json = json.loads(result.text)
    json_keys = result_json.keys()
    if JSON_KEY_DATA in json_keys and len(result_json[JSON_KEY_DATA]):
        data.extend(result_json[JSON_KEY_DATA])
    if JSON_KEY_PAGING in json_keys and JSON_KEY_NEXT in result_json[JSON_KEY_PAGING]:
        next = result_json[JSON_KEY_PAGING][JSON_KEY_NEXT]
        if next:
            getPagedData(access_token, next, data)
    return data

def getJsonData(access_token, endpoint):
    headers = buildHeader(access_token)
    result = requests.get(endpoint,headers=headers)
    result_json = json.loads(result.text)
    return result_json
    

def buildHeader(access_token):
    return {'Authorization': 'Bearer ' + access_token}


#Now get all the groups for the community, then the posts in each group
raw_groups= getCommunityGroups(ACCESS_TOKEN,'112511455959143')
all_groups=[]
for group in raw_groups['groups']['data']:
    all_groups.append(group)
    #now we create a 'feed' field inside the dictionary and add the data
    group['feed']=getLimitedGroupFeed(ACCESS_TOKEN, group['id'])

     
#with open(completeName, 'w') as outfile:
        #json.dump(all_groups, outfile, indent=4)

#Now get all the comments for each of those posts
for group in all_groups:
    for post in group['feed']['feed']['data']:
        for edge in POST_EDGES:
            post[edge]=getPostSummary(ACCESS_TOKEN, post['id'],edge)

completeName = os.path.join(SAVE_PATH, 'GroupwisePostsData.json')
with open(completeName, 'w') as outfile:
    json.dump(all_groups, outfile, indent=4)