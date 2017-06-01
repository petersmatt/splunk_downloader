import requests, urllib
from bs4 import BeautifulSoup, SoupStrainer
import re, os


class splunkFile:

    def __init__(self, url):
        self.url = url
        self.url_parts = re.split(r'/+', url)

    def platform(self):
        #extract directory from url
        return self.url_parts[6]

    def filename(self):
        #extract directory from url
        return self.url_parts[7]

    def newfilename(self):
        newfilename = re.sub(r'spl\w+-[\d\.]+-\w+','splunk-latest',self.filename())
        return  newfilename

    def product(self):
        return self.url_parts[3]


def downloadIsNew(path,filename):
    #if filename is in raw, don't download
    result = True
    if os.path.exists(os.path.join(path,'installs.log')):
        with open(os.path.join(path,'installs.log'),'r') as log:
            if filename in log.read():
                result = False
    return result

def createDiretoryIfNotExists(path):
    if not os.path.exists(path):
        os.mkdir(path)

def generateDirectories(root):
    createDiretoryIfNotExists(os.path.join(root,'installs')) #create installs directory
    createDiretoryIfNotExists(os.path.join(root,'installs','universalforwarder')) #create splunk forwarder dir
    createDiretoryIfNotExists(os.path.join(root,'installs','splunk')) #create splunk forwarder dir


def downloadRename(url,root):
    fil = splunkFile(url)
    installs_path = os.path.join(root,'installs')
    if downloadIsNew(installs_path,fil.filename()):
        path = os.path.join(root,'installs',fil.product(),fil.platform())
        createDiretoryIfNotExists(path)
        newfile = urllib.URLopener()
        newfile.retrieve(url, os.path.join(path,fil.newfilename()))
        with open(os.path.join(installs_path,'installs.log'),'a') as log:
            log.write(fil.filename()+'\n')


def extractFileLinks(url):
    #download page data
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'lxml')
    links = []
    for link in soup.findAll('a', attrs={'data-link': re.compile("^https://")}):
        links.append(link['data-link'])
    return links


urls = [
    'https://www.splunk.com/en_us/download/splunk-enterprise.html',
    'https://www.splunk.com/en_us/download/universal-forwarder.html'
]

root_dir = 'splunk'
createDiretoryIfNotExists(root_dir)
generateDirectories(root_dir)



for url in urls:
    links = extractFileLinks(url)
    for link in links:
        downloadRename(link,root_dir)