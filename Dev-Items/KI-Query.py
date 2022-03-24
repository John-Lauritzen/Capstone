import requests

url = 'https://kitsu.io/api/edge/manga?fields%5Bcategories%5D=slug%2Ctitle&filter%5Bslug%5D=berserk&include=categories'

response = requests.get(url)
print(response.text)