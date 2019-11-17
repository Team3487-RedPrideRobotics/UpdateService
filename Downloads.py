import json
import requests
import tarfile
import os
import urllib

def detar(temp):
    tar = tarfile.open(temp)
    tar.extractall("./extractions")

def getDownloadLink(repo, tag=None):
    #downloads release to temp
    #returns temporary file
    #TODO write version list for each service, server for all versions of software
    #does it delete all data or does it do something else, like backing up the data

    url = 'https://api.github.com/repos/Team3487-RedPrideRobotics/{}/releases'
    url = url.format(repo)
    print(url)
    response = requests.get(url=url.format(repo))
    
    data = response.json()
    
    version = data[0]

    for release in data:
        if release['tag_name'] == tag:
            version = release
            break
    #file_name = data[0]['assets'][0]['name']

    download_url = version['tarball_url']
    return urllib.request.urlretrieve(download_url)
