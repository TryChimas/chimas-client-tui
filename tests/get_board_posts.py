import requests
from requests.auth import HTTPBasicAuth

host = "http://127.0.0.1:41345"
authdata = ("admin","abc123")

#r = requests.get(host+"/posts?where=\{'board_id':'first board','reply_to_id':'0'\}", auth=authdata)
r = requests.get(host+"/posts?where={\"board_id\":\"first board\"}", auth=authdata)
r = requests.get(host+"/posts?where={\"board_id\":\"first board\",\"topic_id\":\"1\"}", auth=authdata)

print(r.text)
