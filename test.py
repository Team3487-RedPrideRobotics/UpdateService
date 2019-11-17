import json
import requests
import tarfile
import os
import urllib

def detar(temp):
    tar = tarfile.open(temp)
    tar.extractall("./extractions")

def downloadRepo(repo):
    #downloads release to temp
    #returns temporary file

    url = 'https://api.github.com/repos/Team3487-RedPrideRobotics/{}/releases'
    url = url.format(repo)
    print(url)
    response = requests.get(url=url.format(repo))
    
    data = response.json()
    
    download_url = data[0]['tarball_url']
    #file_name = data[0]['assets'][0]['name']
    file_name, headers = urllib.request.urlretrieve(download_url)
    detar(file_name)
