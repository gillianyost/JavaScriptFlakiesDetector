# import requests
# from bs4 import BeautifulSoup

# from github import Github
# import sys
# import config
# import time



# repo = sys.argv[1]
# page_num = 30
# #for tensorflow prob
# #url = 'https://github.com/{0}/network/dependents?package_id=UGFja2FnZS01MjYzNzEzMQ%3D%3D'.format(repo)

# url = 'https://github.com/pkgjs/dependents/network/dependents'.format(repo)
# deps=dict()

# def getText(t):
#     try:
#         return "{}/{}".format(
#         t.find('a', {"data-repository-hovercards-enabled": ""}).text,
#         t.find('a', {"data-hovercard-type": "repository"}).text
#     )
#     except:
#         return ""

# while True:
#     #print("GET " + url)
#     r = requests.get(url, auth=(config.username,config.token))

#     soup = BeautifulSoup(r.content, "html.parser")

import requests
from bs4 import BeautifulSoup
from github import Github

repo = "expressjs/express"
url = 'https://github.com/pkgjs/dependents/network/dependents'.format(repo)
nextExists = True
result = []


deps=dict()
g = Github("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")

def getText(t):
    try:
        return "{}/{}".format(
        t.find('a', {"data-repository-hovercards-enabled": ""}).text,
        t.find('a', {"data-hovercard-type": "repository"}).text
    )
    except:
        return ""


while nextExists:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    data = filter(lambda x:len(x) > 0, [getText(t) for t in soup.findAll("div", {"class": "Box-row"})])

    # print(data)
    # print("TEST")
    for d in data:
        repot = g.get_repo(d)
        if repot.stargazers_count > 1:
            print(d, repot.stargazers_count, "http://github.com/{0}".format(d))
            deps[d]=repot.stargazers_count
    # print(len(data))
    # print("TEST")
    try:
        url = soup.find("div", {"class":"paginate-container"}).findAll('a')
        assert "dependents_after" in url
    except:
        import traceback as tb
        tb.print_exc()
        break
print(sorted(deps.keys(), key=lambda x: deps[x]))
