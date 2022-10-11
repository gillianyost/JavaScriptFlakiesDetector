import requests
from bs4 import BeautifulSoup

from github import Github
import sys
# import config
import time
from urllib.request import urlopen


g = Github("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")

# repo = sys.argv[1]
page_num = 30
#for tensorflow prob
#url = 'https://github.com/{0}/network/dependents?package_id=UGFja2FnZS01MjYzNzEzMQ%3D%3D'.format(repo)

url = urlopen("https://github.com/pkgjs/dependents/network/dependents")

# url = 'https://github.com/search?l=&o=desc&q=stars%3A%3E1+language%3AJavaScript&s=stars&type=Repositories'.format(repo)
# print("GET " + url)
deps=dict()
nextExists = True

def getText(t):
    try:
        return "{}/{}".format(
        t.find('a', {"data-repository-hovercards-enabled": ""}).text,
        t.find('a', {"data-hovercard-type": "repository"}).text
    )
    except:
        return ""
counter = 0
while nextExists:
    # time.sleep(1)
    if counter > 4000:
        time.sleep(3600)
        counter = 0
    counter = counter + 1
    # print("GET " + url)
    r = requests.get(url, auth=("gillianyost","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"))

    soup = BeautifulSoup(r.content, "html.parser")

    data = filter(lambda x:len(x) > 0, [getText(t) for t in soup.findAll("div", {"class": "Box-row"})])

    #print(data)
    for d in data:
        # time.sleep(1)
        repot = g.get_repo(d)
        if repot.stargazers_count > 1000:
            print(d, repot.stargazers_count, "http://github.com/{0}".format(d))
            deps[d]=repot.stargazers_count
    #print(len(data))
    nextExists = False
    for u in soup.find("div", {"class":"paginate-container"}).findAll('a'):
        if u.text == "Next":
            nextExists = True
            url = u["href"]
    # try:
    #     url = soup.find("div", {"class":"paginate-container"}).findAll('a')
    #     assert "dependents_after" in url
    # except:
    #     import traceback as tb
    #     tb.print_exc()
    #     break
print(sorted(deps.keys(), key=lambda x: deps[x]))
