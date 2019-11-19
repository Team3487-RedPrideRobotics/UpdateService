import json
import requests
import tarfile
import os
import urllib
import logging

def detar(temp):
    tar = tarfile.open(temp)
    tar.extractall("./extractions")

def getDownloadLink(source,tag=None):
    #downloads release to temp
    #returns temporary file
    #TODO write version list for each service, server for all versions of software
    #does it delete all data or does it do something else, like backing up the data
    logging.info("Given user: {}; Given repo: {}".format(source.user,source.repo))
    
    url = 'https://api.github.com/repos/{}/{}/releases'.format(source.user,source.repo)
    logging.debug("API URL: {}".format(url))
    
    response = requests.get(url=url.format(source.user,source.repo))
    logging.debug("Response: {}".format(response.json()))
    
    data = response.json()
    
    version = data[0]

    for release in data:
        if release['tag_name'] == tag:
            version = release
            break
    #file_name = data[0]['assets'][0]['name']

    download_url = version['tarball_url']
    return urllib.request.urlretrieve(download_url)
