import requests

# Here we define our query as a multi-line string
query = '''
query ($page: Int, $perPage: Int, $search: String, $type: MediaType) {
    Page (page: $page, perPage: $perPage) {
        media (search: $search, type: $type) {
            title {
                romaji
            }
            genres
            tags {
                name
            }
        }
    }
}
'''
variables = {
    'search': 'Berserk',
    'type': 'MANGA',
    'page': 1,
    'perPage': 1
}
url = 'https://graphql.anilist.co'

response = requests.post(url, json={'query': query, 'variables': variables})
print(response.json())



