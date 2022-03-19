class my_class(object):
    pass

# Here we define our query as a multi-line string
query = '''
query ($id: Int, $page: Int, $perPage: Int, $search: String) {
    Page (page: $page, perPage: $perPage) {
        pageInfo {
            total
            currentPage
            lastPage
            hasNextPage
            perPage
        }
        media (id: $id, search: $search) {
            id
            title {
                romaji
            }
        }
    }
}
'''
variables = {
    'search': 'Berserk',
    'page': 1,
    'perPage': 3
}
url = 'https://graphql.anilist.co'
​
response = requests.post(url, json={'query': query, 'variables': variables})
print(response)



