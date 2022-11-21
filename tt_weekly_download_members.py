import requests
import json
import os.path
import datetime

from config import TT_MAIN, TT_COMMUNITY, ACCESS_TOKEN

#This is the common prefix for all calls
GRAPH_URL_PREFIX = 'https://graph.facebook.com/'
#All data resulting from this code will be saved at this link. Please adjust it as per your requirement:
SAVE_PATH='D:\Dropbox\Dropbox\Programming\Trainer_Tribe_Data'

#This section lists suffixes and fields at each level of the data hierarchy 
COMMUNITY_FIELDS='members'

MEMBER_SUFFIX='/members'
MEMBER_FIELDS='id, name, email, locale, account_claim_time'

#This is the universal access token used in all requests in this script

#Adjust how many results you want to stay visible
LIMIT= 500

#This section includes 'conjunctions' in between the clauses so as to form a full HTTP request as per the Workplace API
FIELDS_CONJ = '?fields='
LIMITS_EDGE_CONJ = '?limit='
LIMITS_CONJ='.limit=('+str(LIMIT)+')'

def getCommunityMembers(access_token, community_ID):
"""Extracts the IDs of all the groups that are members of the selected community"""
    endpoint= GRAPH_URL_PREFIX +community_ID+ FIELDS_CONJ + COMMUNITY_FIELDS
    return getJsonData(access_token, endpoint)

def getMemberDetails(access_token, member_ID)
"""Extracts the data of all members of the Trainer Tribe Community"""
	endpoint= GRAPH_URL_PREFIX +member_ID+ FIELDS_CONJ + MEMBER_FIELDS+LIMITS_CONJ


def getJsonData(access_token, endpoint):
    headers = buildHeader(access_token)
    result = requests.get(endpoint,headers=headers)
    result_json = json.loads(result.text)
    return result_json



def getJsonSimpleData(access_token, endpoint):
    headers = buildHeader(access_token)
    result = requests.get(endpoint,headers=headers)
    result_json = json.loads(result.text)
    return result_json['feed']['data']

def buildHeader(access_token):
    return {'Authorization': 'Bearer ' + access_token}


###### CORE DOWNLOADING ########
members_list=[]
get_members=getCommunityMembers(ACCESS_TOKEN, TT_COMMUNITY)
for members in get_members:
	members
