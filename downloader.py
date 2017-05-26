import requests
from bs4 import BeautifulSoup, SoupStrainer
import re


class splunkFile:

    def __init__(self, url):
        self.url = url
        self.url_parts = re.split(r'/+')

    def platform(self):
        #extract directory from url
        return self.url_parts[6]

    def product(self):
        return self.url_parts[3]

    def download(self):
        #download file and place in directory
        #rename to appropriate name
        pass



def extractFileLinks(url):
    #download page data
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'lxml')
    links = []
    for link in soup.findAll('a', attrs={'data-link': re.compile("^https://")}):
        pass
    #loop through tabs
    #extract data links
    #return list of links

    pass

def createFiles(link):
    #download the file
    #change the name to splunk_x_latest

    pass

splunk_enterprise_url = 'https://www.splunk.com/en_us/download/splunk-enterprise.html'
splunk_forwarder_url = 'https://www.splunk.com/en_us/download/universal-forwarder.html'




#for each url
#for each panel
##create a folder with the panel name
##for each file
###download file
###rename each file as splunk_forwarder_latest or splunk_enterprise_latest


