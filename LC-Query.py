import requests

url = 'http://lx2.loc.gov:210/lcdb?version=1.1&operation=searchRetrieve&query=bath.isbn=9781593073305&maximumRecords=1&recordSchema=mods'

response = requests.get(url)
print(response.text)