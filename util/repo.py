from Downloads import getDownloadLink, detar, getDownloadManifest
import shutil
from packaging import version
import logging

class DownloadSource():

    def __init__(self, dicto):
        self.location = dicto['location']
        self.repo = dicto['repo']
        self.tag = dicto['tag']
        self.user = dicto['user']
        

    def compare(self, updated, old):

        if updated.repo != old.repo:
            False

        if updated.location != old.location:
            try:
                shutil.move(old.location, updated.location)
            except FileNotFoundError:
                logging.info("File Not Found")

        if version.parse(updated.tag) != version.parse(old.tag):
            return True
        
        return False