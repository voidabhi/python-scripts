
from hammock import Hammock as Github

github = Github('https://api.github.com')
headers = {'Accept': 'application/vnd.github.preview'}
resp = github.search.repositories.GET(params={'q': 'language:python', 'sort': 'stars', 'per_page': 10, 'page': 1}, headers=headers)
res = resp.json()
print res['items'][0]['full_name']
print len(res['items'])
