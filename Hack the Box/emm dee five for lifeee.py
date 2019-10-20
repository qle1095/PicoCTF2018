import requests
from bs4 import BeautifulSoup
import hashlib
import datetime

s = requests.Session()
page = s.get("http://docker.hackthebox.eu:33295/")
soup = BeautifulSoup(page.content, "html.parser")
text = str(soup.find("h3").text)
hash = hashlib.md5(text.encode("utf")).hexdigest()
print(text)
print(hash)
data = {"hash": hash}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
}
postResponse = s.post(
    "http://docker.hackthebox.eu:33295/", data=data, headers=headers
)
content = BeautifulSoup(postResponse.content, "html.parser")
print(postResponse.headers)
print(content)
