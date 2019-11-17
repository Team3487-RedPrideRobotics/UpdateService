from Downloads import getDownloadLink, detar

    #TODO get list of libraries to update
    # - Their locations in system
    # - The link to download them
    # - The service associated with it (if linux)
    # - Download executable or python
    # - Command Line Arguments
    # - Checks for updates
    # - When done; closes

if __name__ == "__main__":

    #check for updates (txt file on website or dns records?)
    #compare current versions
    #stops old services
    #download & extract new versions
    #modifies systemd service if necessary (assets on github)
    #restarts services
    filename, headers = getDownloadLink(repo="UpdateService")
    detar(filename)
    
