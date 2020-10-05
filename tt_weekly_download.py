import requests
import json
import os.path
import datetime

#This is the common prefix for all calls
GRAPH_URL_PREFIX = 'https://graph.facebook.com/'
#All data resulting from this code will be saved at this link:
SAVE_PATH='D:\Dropbox\Dropbox\Programming\Trainer_Tribe_Data'

#This section lists suffixes and fields at each level of the data hierarchy 
COMMUNITY_FIELDS='groups'

GROUPS_SUFFIX = '/groups'
GROUP_FIELDS = 'id,name,members,privacy,description,updated_time'

FEED_SUFFIX= '/feed'

POST_FIELDS= 'from,type'
POST_EDGES= ['attachments','comments', 'likes','seen']


#Adjust how many results you want to stay visible
FEED_LIMIT= 500
DAYS= 7
SINCE = datetime.datetime.now() - datetime.timedelta(days=DAYS)

#This section includes 'conjunctions' in between the clauses so as to form a full HTTP request as per the Workplace API
FIELDS_CONJ = '?fields='
LIMITS_EDGE_CONJ = '?limit='
LIMITS_CONJ='.limit=('+str(FEED_LIMIT)+')'
SUMMARY_REQUEST='?summary=true'



#This is the universal access token used in all requests in this script.
ACCESS_TOKEN= 'DQVJ2LTNQa3B0M3dra1hfdTJnT2YyNmw2X0cxUHJlMWFtWW9XWW9pbDdSVkJYYkNqMlFfb0RidTU4anRXM3E5LTU2MHFsZA2hnSGZAYUEhPOHBTTGpfYlk3UUh4S2xzX1VMeF9VNkk0cjFvd09hRFlpR21DcERqUlRaYjZAIT3BfcFY1Ry1OVWJsZAkdzS21mSG1xVkZAtb1FSbFU0UDZAUM0wwWTE2TlBpY3VpSmQxd2M5eFlSWmVScnBxbmVIYl9QZAGZASNUw1bDhR'
TT_MAIN="284578622020844"

#The functions below extract the fields listed above at the required level of the hierarchy

def getCommunityGroups(access_token, community_ID):
    """Extracts the IDs of all the groups that are members of the selected community"""
    endpoint= GRAPH_URL_PREFIX +community_ID+ FIELDS_CONJ + COMMUNITY_FIELDS
    return getJsonData(access_token, endpoint)

def getLimitedGroupFeed(access_token, group_id):
    """Extracts all posts from that community, within the maximum limit of the number of posts provided by the user"""
    endpoint = GRAPH_URL_PREFIX + group_id + FIELDS_CONJ+'feed'+ LIMITS_CONJ 
    print(endpoint)
    return getJsonSimpleData(access_token, endpoint)

def getPostFields(access_token, post_id):
    "Gets information on the requested fields for the given post"
    endpoint= GRAPH_URL_PREFIX + post_id +FIELDS_CONJ +POST_FIELDS
    return getJsonData(access_token, endpoint)

def getPostSummary(access_token, post_id, summary_type):
    "Gets information on the comments, reactions or likes to a given post, as per what the user specifies"
    endpoint= GRAPH_URL_PREFIX + post_id +"/" +summary_type
    return getJsonEdgeData(access_token, endpoint)

#These functions return the Get API requests and convert them into the required JSON format
def getJsonData(access_token, endpoint):
    headers = buildHeader(access_token)
    result = requests.get(endpoint,headers=headers)
    result_json = json.loads(result.text)
    return result_json

def getJsonEdgeData(access_token, endpoint):
    headers = buildHeader(access_token)
    result = requests.get(endpoint,headers=headers)
    result_json = json.loads(result.text)
    return result_json['data']

def getJsonSimpleData(access_token, endpoint):
    headers = buildHeader(access_token)
    result = requests.get(endpoint,headers=headers)
    result_json = json.loads(result.text)
    return result_json['feed']['data']

def buildHeader(access_token):
    return {'Authorization': 'Bearer ' + access_token}


###################START DOWNLOAD ###############

#Now get all the groups for the community, then the posts in each group
raw_groups= getCommunityGroups(ACCESS_TOKEN,'112511455959143')
all_groups=[]
for group in raw_groups['groups']['data']:
    all_groups.append(group)
    #now we create a 'feed' field inside the dictionary and add the data
    group['posts']=getLimitedGroupFeed(ACCESS_TOKEN, group['id'])
    
#Now get all the comments for each of those posts
for group in all_groups:
    for post in group['posts']:
        post['details']= getPostFields(ACCESS_TOKEN, post['id'])
        for edge in POST_EDGES:
            post[edge]=getPostSummary(ACCESS_TOKEN, post['id'],edge)

completeName = os.path.join(SAVE_PATH, 'GroupwisePostsData.json')
with open(completeName, 'w') as outfile:
    json.dump(all_groups, outfile, indent=4)