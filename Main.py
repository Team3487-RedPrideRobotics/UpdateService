from util.repo import DownloadSource
from Downloads import getDownloadManifest, cleanup, getDownloadLink, detar
import os
import requests
import json
import logging

    #TODO get list of libraries to update
    # - Their locations in system
    # - The link to download them
    # - The service associated with it (if linux)
    # - Download executable or python
    # - Command Line Arguments
    # - Checks for updates
    # - When done; closes

def big_web(web, mani_entries):
    for i in range(0, len(mani_entries)):
        exist = True
        changes = False
        d_entry = DownloadSource(list(web.values())[0])
        try:
            m_entry = DownloadSource(mani_entries[d_entry.user+d_entry.repo])
        except KeyError:
            changes = True
            exist = False
        if not changes:
            changes = DownloadSource.compare(d_entry,d_entry,m_entry)

        if(changes):
            filename, headers = getDownloadLink(d_entry)
            detar(filename, d_entry.location)

        del web[d_entry.user+d_entry.repo]
        if exist:
            del mani_entries[m_entry.user+m_entry.repo]

    for entry in web:
        web[entry] = DownloadSource(web[entry])
    cleanup(mani_entries, web)

def big_mani(web, mani_entries):
    
    for i in range(0, len(web)):
        changes = False
        d_entry = DownloadSource(web[list(web.keys())[0]])
        m_entry = DownloadSource(mani_entries[d_entry.user+d_entry.repo])

        changes = DownloadSource.compare(d_entry,d_entry,m_entry)

        if(changes):
            filename, headers = getDownloadLink(d_entry)
            detar(filename, d_entry.location)

        del web[d_entry.user+d_entry.repo]
        del mani_entries[m_entry.user+m_entry.repo]

    for entry in web:
        web[entry] = DownloadSource(web[entry])
    cleanup(mani_entries, web)

if __name__ == "__main__":
    logging.basicConfig(filename='testing.log',level=logging.DEBUG)
    manifest, exists = getDownloadManifest()   

    link = os.getenv('QIRAFACE')
    if link is None:
        link = "https://api.bak3dnet.net/false.json"
    logging.info("Download API link = %s" % link)
    update_document = requests.get(link)
    logging.info("Status code %s" % update_document.status_code)

    if (not exists) and update_document.status_code > 299:
        logging.error("Could not find update documents.")
        logging.info("No updates generated")
        exit(1)

    if not update_document.status_code > 299:
        logging.debug("Document: %s" % update_document.json())
        web = update_document.json()

        logging.info("Mani-entries %s"%len(manifest))
        logging.info("web entries: %s" % len(web))
        logging.info(web)

        if len(web) > len(manifest):
            big_web(web, manifest)
        else:
            big_mani(web, manifest)

        with open("update_list.json", "w+") as manifest:
            json.dump(update_document.json(), manifest)
    
    
    #check for updates (txt file on website or dns records?)
    #compare current versions
    #stops old services
    #download & extract new versions
    #modifies systemd service if necessary (assets on github)
    #restarts services

    