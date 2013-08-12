import re, urllib, urllib2

# Download Google spreadsheet
class Spreadsheet(object):
    def __init__(self, key):
        super(Spreadsheet, self).__init__()
        self.key = key

class Client(object):
    def __init__(self, email, password):
        super(Client, self).__init__()
        self.email = email
        self.password = password

    def _get_auth_token(self, email, password, source, service):
        url = "https://www.google.com/accounts/ClientLogin"
        params = {
            "Email": email, "Passwd": password,
            "service": service,
            "accountType": "HOSTED_OR_GOOGLE",
            "source": source
        }
        req = urllib2.Request(url, urllib.urlencode(params))
        return re.findall(r"Auth=(.*)", urllib2.urlopen(req).read())[0]

    def get_auth_token(self):
        source = type(self).__name__
        return self._get_auth_token(self.email, self.password, source, service="wise")

    def download(self, spreadsheet, gid=1, format="csv"):
        url_format = "https://spreadsheets.google.com/feeds/download/spreadsheets/Export?key=%s&exportFormat=%s&gid=%i"
        headers = {
            "Authorization": "GoogleLogin auth=" + self.get_auth_token(),
            "GData-Version": "3.0"
        }
        req = urllib2.Request(url_format % (spreadsheet.key, format, gid), headers=headers)
        return urllib2.urlopen(req)

if __name__ == "__main__":
    import getpass
    import csv

    email = "leftwich@umich.edu" 
    password = getpass.getpass()
	
    spreadsheet_id = "0AinMDATKswMWdGJraFQtRTBMSWt3bFgzRjV4clZuNUE" # (spreadsheet id here)

    # Create client and spreadsheet objects
    gs = Client(email, password)
    ss = Spreadsheet(spreadsheet_id)

    # Request a file-like object containing the spreadsheet's contents
    csv_file = gs.download(ss)

    # Parse as CSV and print the rows
    # for row in csv.reader(csv_file):
    #    print ", ".join(row)
		

# now do the scraping

# imports		
import csv 
import urllib2
import re
from bs4 import BeautifulSoup
import mechanize
import imghdr

# get urls from csv object we just downloaded and start loop
urls = csv.reader(csv_file)
for url in urls:
    response = urllib2.urlopen(url[0])
    fullHTML = response.read()


    # put it into BeautifulSoup
    soup = BeautifulSoup(fullHTML)
	
    #remove images
    images = soup.findAll('img')
    for image in images:
        image.extract()
		

	# get the h1 and the main content div (id = content-core)
	# ...make them into strings and add them together
	# ...this is partialHTML
	# ...there's probably a better way to do this
    headerHandler = soup.find("h1")
    header = headerHandler.prettify('latin-1')
    contentHandler = soup.find("div", {"id": "content-core"})
	
    # get rid of classes in content
    for tag in contentHandler.findAll():
        del tag['class']
        del tag['style']

    # if there are links, log that this page needs some attention
    for link in contentHandler.findAll('a'):
        linkStatus = 'needs links specified'


	
	
    content = contentHandler.prettify('latin-1')
    headerstring = str(header).replace('<h1>', '<h2>').replace('</h1>', '</h2>')
    contentstring = str(content).replace('<div id="content-core">', '').replace('</div>', '')

	
    partialHTML = headerstring + contentstring




    # Get title and remove special characters to make a valid filename
    pageTitle = soup.title.string
    filename = "".join([c for c in pageTitle if re.match(r'\w', c)])
	

	# Specify path to files
    from os.path import join as pjoin
    path_to_folder = pjoin('C:\\', 'Users', 'leftwich', 'Documents', 'scraper', 'che')


	
	# Write each filename to a .txt file to be used later by iMacros
	# ...this may not be necessary, will prob upload them manually
	# ...Possibly useful as documentation.
    logFile = open(path_to_folder + '\\' + 'urls.txt', 'a')
    logFile.write ('"' + filename + '.html' + '"' + ',' + '"' + linkStatus + '"' + '\n')
    
    
    # Now write the partialHTML to file in current folder
    partialPageFile = open(path_to_folder + '\\' + filename + '.html', 'w+')
    partialPageFile.write (partialHTML)
    partialPageFile.close()	

    from time import sleep
    sleep(3) # Time in seconds.

# Close text file with list of filenames	
logFile.close()
	

	
	
	
# Lastly, be sure that your URLs are properly formed:
# C:\Users\leftwich\Documents\scraper\
# http://www.cnn.com
# http://www.fark.com
# http://www.cbc.ca

# todo
# 1. [DONE] with BS, process each page to retain only the header and main content
# 2. [DONE] save a copy of the processed content as a standalone page
# 3. [DONE] save a copy of the unprocessed content as a standalone page
# 4.        get url list from kate/jennifer/esther
# 5.        upload processed pages to google docs (manually, only happens once)
# 6.        write new script to download and process google docs into clean html

# to get image links

# links = soup.findAll('img', src=True)
# for link in links:
#     print link['src']
