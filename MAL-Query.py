import requests

url = 'https://api.myanimelist.net/v2/manga/2?fields=id,title,genres'
headers = {'X-MAL-CLIENT-ID': '8e63b628fd74b0bab02e703f52e79743'}

response = requests.get(url, headers=headers)
print(response.json())