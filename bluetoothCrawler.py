import os
import errno
import ssl
import re
import xmltodict
import pprint
import json
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

url = "https://www.bluetooth.com/specifications/gatt/services/"
prefixUrl = "https://www.bluetooth.com"
urls = []
names = []
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
req = Request(url, headers=headers)
#Get the web page
gcontext = ssl.SSLContext()
webpage = urlopen(req, context=gcontext).read()
page_soup = BeautifulSoup(webpage, "html.parser")
for a in page_soup.find_all('a', href=True):
    link = a['href']
    fullUrl = prefixUrl + link
    if fullUrl.endswith('.xml'):
        urls.append(fullUrl)
        name = re.search('(?<=/Services/).*(?=.xml)', fullUrl)
        names.append(name.group(0))
    #endif    
#end for
names_urls = zip(names, urls)

for name, url in names_urls:
    print(name)
    print(url)
    file_name = "xml_files/" + name + ".xml"
    rq = Request(url, headers=headers)
    res = urlopen(rq, context=gcontext)
    xml_string = res.read()
    # check if dir exists
    if not os.path.exists(os.path.dirname(file_name)):
        try:
            os.makedirs(os.path.dirname(file_name))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise 
            #endif
        #end try
    #endif
    file = open(file_name, "wb")
    #xml to json parser is not working as expected
    #xml_parsed = xmltodict.parse(xml_string)
    #file.write(json.dumps(xml_parsed).encode('utf-8'))
    file.write(xml_string)
    file.close()
#end for