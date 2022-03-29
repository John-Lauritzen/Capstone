import requests
import xml.etree.ElementTree as ET
import json
import string
import Database as DB

InvalidPunctuation = string.punctuation.replace('-','')
MALheaders = {'X-MAL-CLIENT-ID': '8e63b628fd74b0bab02e703f52e79743'}

def LCquery(ISBN):
    """
    Get volume title from the Library of Congress using the ISBN
    :param ISBM: The ISBN to be used as a string
    :return: Title as a string
    """
    #Library of Congress query
    LCurl = 'http://lx2.loc.gov:210/lcdb?version=1.1&operation=searchRetrieve&query=bath.isbn='+ ISBN +'&maximumRecords=1'
    LCresponse = requests.get(LCurl)
    #Get XML format data
    LCdata = LCresponse.text
    #Convert data
    LCresult = ET.fromstring(LCdata)
    #Find Title tag
    try:
        LCtitle = LCresult[2][0][2][0].findall(".//*[@tag='245']/")
    except:
        return 0
    #Store title value
    VolTitle = LCtitle[0].text.strip(' /')
    return VolTitle

def MALquery(title):
    """
    Get series information from MyAnimeList.net using title
    :param title: Title of the series as a string
    :return: List of the updated title and tags
    """
    #Remove : character as it causes problems
    Cleantitle = str(title).translate(str.maketrans('', '', InvalidPunctuation))
    #MAL Query 1
    MALurl = 'https://api.myanimelist.net/v2/manga?q='+ Cleantitle
    MALresponse1 = requests.get(MALurl, headers=MALheaders)
    #Get data
    MALquery = MALresponse1.text
    #Convert data
    MALqueryresult = json.loads(MALquery)
    #Get first ID
    try:
        MALtopID = str(MALqueryresult['data'][0]['node']['id'])
    except:
        return 0
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
    MALdatafinal = list()
    MALdatafinal.append(MALdata['title'])
    for item in MALdata['genres']:
        MALdatafinal.append(item['name'])
    return MALdatafinal

def KIquery(MALtitle):
    """
    Get series information from Kitsu.io using title from MyAnimeList.net
    :param title: Title of the series from MyAnimeList.net
    :return: List of tags
    """
    #Convert MAL title for use with KI
    KItitleclean = str(MALtitle).translate(str.maketrans('', '', InvalidPunctuation))
    KItitle = KItitleclean.replace(' ', '-')
    #Query KI
    KItempurl = 'https://kitsu.io/api/edge/manga?fields%5Bcategories%5D=slug%2Ctitle&filter%5Bslug%5D='+ KItitle +'&include=categories'
    #Get data
    KItempresult = requests.get(KItempurl)
    #Convert data
    KItempdata = json.loads(KItempresult.text)
    #Check if data returned
    if KItempdata['meta']['count'] == 0:
        return 0
    else:
        #Check if a Novel or Manga was returned
        if KItempdata['data'][0]['attributes']['subtype'] == 'novel':
            #If novel returne
            KIurl = 'https://kitsu.io/api/edge/manga?fields%5Bcategories%5D=slug%2Ctitle&filter%5Bslug%5D='+ KItitle +'-manga&include=categories'
            KIresult = requests.get(KIurl)
            #Convert data
            KIdata = json.loads(KIresult.text)
        else:
            KIdata = KItempdata
    #Check if data returned
    if KIdata['meta']['count'] == 0:
        return 0
    else:
        KIdatafinal = list()
        try:
            for item in KIdata['included']:
                KIdatafinal.append(item['attributes']['title'])
        except:
            return 0
        return KIdatafinal

def ALquery(MALtitle):
    """
    Get series information from AniList.co using title from MyAnimeList.net
    :param title: Title of the series from MyAnimeList.net
    :return: List of tags
    """
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
        'search': MALtitle,
        'type': 'MANGA',
        'page': 1,
        'perPage': 1
    }
    ALurl = 'https://graphql.anilist.co'
    #Query AL
    ALresult = requests.post(ALurl, json={'query': ALquery, 'variables': ALvariables})
    #Store data
    ALdata = ALresult.json()
    #Check if data was returned
    try:
        ALdatafinal = list()
        for item in ALdata['data']['Page']['media'][0]['genres']:
            ALdatafinal.append(item)
        for item in ALdata['data']['Page']['media'][0]['tags']:
            ALdatafinal.append(item['name'])
        return ALdatafinal
    except:
        return 0

def get_trending():
    '''
    Queries MAL for list of at least 20 trending manga that are not owned
    :return: List of titles by popularity that are not owned
    '''
    Trending = list()
    #Initial MAL URL
    MALurl = 'https://api.myanimelist.net/v2/manga/ranking?ranking_type=bypopularity&limit=20'
    while len(Trending) < 20:
        #MAL Query
        MALresponse1 = requests.get(MALurl, headers=MALheaders)
        #Get data
        MALquery = MALresponse1.text
        #Convert data
        MALqueryresult = json.loads(MALquery)
        conn = DB.create_connection()
        Owned = DB.get_ownedseries(conn)
        for i in range(19):
            #Get ID
            MALID = str(MALqueryresult['data'][i]['node']['id'])
            #Query media type of ID
            MALlisturl = 'https://api.myanimelist.net/v2/manga/'+ MALID +'?fields=media_type'
            MALlistresponse = requests.get(MALlisturl, headers=MALheaders)
            #Get data
            MALlistresult = json.loads(MALlistresponse.text)
            #Check if ID is manga and unowned
            if str(MALlistresult['media_type']) == 'manga' and str(MALlistresult['title']) not in Owned:
                Trending.append(MALlistresult['title'])
        MALurl = MALqueryresult['paging']['next']
    
    return Trending
        

