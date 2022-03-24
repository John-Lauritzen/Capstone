import requests
import xml.etree.ElementTree as ET
import json
import string

ISBN = '9781975357399'
InvalidPunctuation = string.punctuation.replace('-','')

#Library of Congress query
LCurl = 'http://lx2.loc.gov:210/lcdb?version=1.1&operation=searchRetrieve&query=bath.isbn='+ ISBN +'&maximumRecords=1'
LCresponse = requests.get(LCurl)
#Get XML format data
LCdata = LCresponse.text
#Convert data
LCresult = ET.fromstring(LCdata)
#Find Title tag
LCtitle = LCresult[2][0][2][0].findall(".//*[@tag='245']/")
#Store title value
VolTitle = LCtitle[0].text.strip(' /')

#MAL Query 1
MALurl = 'https://api.myanimelist.net/v2/manga?q='+ VolTitle
MALheaders = {'X-MAL-CLIENT-ID': '8e63b628fd74b0bab02e703f52e79743'}
MALresponse1 = requests.get(MALurl, headers=MALheaders)
#Get data
MALquery =MALresponse1.text
#Convert data
MALqueryresult = json.loads(MALquery)
#Get first ID
MALtopID = str(MALqueryresult['data'][0]['node']['id'])
#Query media type of first ID
MALtopurl = 'https://api.myanimelist.net/v2/manga/'+ MALtopID +'?fields=media_type'
MALtopresponse = requests.get(MALtopurl, headers=MALheaders)
#Get data
MALtopresult = json.loads(MALtopresponse.text)
#Check if first ID is manga
if str(MALtopresult['media_type']) == 'manga':
    MALid = MALtopID
else:
    #Check if first and second titles match
    if str(MALqueryresult['data'][0]['node']['title']) == str(MALqueryresult['data'][1]['node']['id']):
        #Get 2nd ID
        MAL2ndID = str(MALqueryresult['data'][1]['node']['id'])
        #Query media type for 2nd ID
        MAL2ndurl = 'https://api.myanimelist.net/v2/manga/'+ MAL2ndID +'?fields=media_type'
        MAL2ndresponse = requests.get(MALtopurl, headers=MALheaders)
        #Get data
        MAL2ndresult = json.loads(MAL2ndresponse.text)
        #Check if 2nd ID is manga
        if str(MAL2ndresult['media_type']) == 'manga':
            #Assign ID as 2nd as it is the manga
            MALid = MAL2ndID
        else:
            #Assign ID as top as both are not manga
            MALid = MALtopID
    else:
        #Assign ID as top since 2nd does not have the same title
        MALid = MALtopID
#Query details for final ID
MALfinalurl = 'https://api.myanimelist.net/v2/manga/'+ MALid +'?fields=id,title,genres'
MALfinalresponse = requests.get(MALfinalurl, headers=MALheaders)
#Get data
MALdata = json.loads(MALfinalresponse.text)

#Convert MAL title for use with KI
KItitleclean = str(MALdata['title']).translate(str.maketrans('', '', InvalidPunctuation))
KItitle = KItitleclean.replace(' ', '-')
#Query KI
KItempurl = 'https://kitsu.io/api/edge/manga?fields%5Bcategories%5D=slug%2Ctitle&filter%5Bslug%5D='+ KItitle +'&include=categories'
#Get data
KItempresult = requests.get(KItempurl)
#Convert data
KItempdata = json.loads(KItempresult.text)
#Check if a Novel or Manga was returned
if KItempdata['data'][0]['attributes']['subtype'] == 'novel':
    #If novel returne
    KIurl = 'https://kitsu.io/api/edge/manga?fields%5Bcategories%5D=slug%2Ctitle&filter%5Bslug%5D='+ KItitle +'-manga&include=categories'
    KIresult = requests.get(KIurl)
    #Convert data
    KIdata = json.loads(KIresult.text)
else:
    KIdata = KItempdata

#Define AL Query
ALquery = '''
query ($page: Int, $perPage: Int, $search: String, $type: MediaType) {
    Page (page: $page, perPage: $perPage) {
        media (search: $search, type: $type) {
            genres
            tags {
                name
            }
        }
    }
}
'''
ALvariables = {
    'search': VolTitle,
    'type': 'MANGA',
    'page': 1,
    'perPage': 1
}
ALurl = 'https://graphql.anilist.co'
#Query AL
ALresult = requests.post(ALurl, json={'query': ALquery, 'variables': ALvariables})
#Store data
ALdata = ALresult.json()

#Return title and MAL genres
print('MyAnimeList.net Data')
print(MALdata['title'])
for item in MALdata['genres']:
    print(item['name'])
#Return KI categories
print('Kitsu.io Data')
for item in KIdata['included']:
    print(item['attributes']['title'])
#Return AL categories
print('AniList.co Data')
for item in ALdata['data']['Page']['media'][0]['genres']:
    print(item)
for item in ALdata['data']['Page']['media'][0]['tags']:
    print(item['name'])