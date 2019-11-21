import json
import requests
import tarfile
import os
import urllib
import logging
import shutil

def detar(temp,location):
    tar = tarfile.open(temp)
    try:
        shutil.rmtree(location)
    except FileNotFoundError:
        logging.info("Creating Dir")
    tar.extractall(location)
    logging.info(os.listdir(location))
    old = os.path.join(location,os.listdir(location)[0])
    files = os.listdir(old)
    for f in files:
        logging.info(os.path.join(old,f))
        shutil.move(os.path.join(old,f),location)
    shutil.rmtree(old)

def getDownloadManifest():
    with open('update_list.json', 'r') as manifest:
        manifestData = manifest.read()
        logging.info("Manifest length: %s"% len(manifestData))
        try:
            data = json.loads(manifestData)
            return data, True
        except json.decoder.JSONDecodeError:
            return {"ab":{'user':'a','repo':'b','tag':'c','location':'d'}}, False

def getDownloadLink(source):
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
        if release['tag_name'] == source.tag:
            version = release
            break
    #file_name = data[0]['assets'][0]['name']

    download_url = version['tarball_url']
    return urllib.request.urlretrieve(download_url)

def cleanup(mani_entries, web):
    #delete old software
    for i in range(0, len(mani_entries)):
        try:
            shutil.rmtree(list(mani_entries.values())[i]['location'])
        except FileNotFoundError:
            logging.info("No file found")

    #download new software
    for entry in web:
        filename, headers = getDownloadLink(web[entry])
        detar(filename, web[entry].location)
