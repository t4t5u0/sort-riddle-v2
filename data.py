import requests

link = 'https://ja.wikipedia.org/w/api.php?action=query&list=random&format=json'
response = requests.get(link)
json_data = response.json()
print(json_data['query']['random'][0]['title'])