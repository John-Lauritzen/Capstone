import requests
import xml.etree.ElementTree as ET
import json
import string

ISBN = '9781975339838'

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
    print('Manga not first result')
#Query details for first ID
MALfinalurl = 'https://api.myanimelist.net/v2/manga/'+ MALtopID +'?fields=id,title,genres'
MALfinalresponse = requests.get(MALfinalurl, headers=MALheaders)
#Get data
MALdata = json.loads(MALfinalresponse.text)
#Return title and genres
print(MALdata['title'], MALdata['genres'])

#Convert MAL title for use with KI
KItitleclean = str(MALdata['title']).translate(str.maketrans('', '', string.punctuation))
KItitle = KItitleclean.replace(' ', '-')
#Query KI
KIurl = 'https://kitsu.io/api/edge/manga?fields%5Bcategories%5D=slug%2Ctitle&filter%5Bslug%5D='+ KItitle +'&include=categories'
#Get data
KIresult = requests.get(KIurl)
#Convert data
KIdata = json.loads(KIresult.text)
#Return categories
print(KIdata['included'])


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

response = requests.post(ALurl, json={'query': ALquery, 'variables': ALvariables})
print(response.json())