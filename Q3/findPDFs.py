from bs4 import BeautifulSoup #for parsing html
import requests #for getting final uri
import random # used for User Agent Function
import sys #for command line argments
import re # for regex method of validating PDFs
from urllib.parse import urljoin  # for converting relative to absolute paths

#code for handling user-agent to deal with some webservers
#GET_UA() code derived from 
# https://www.jcchouinard.com/random-user-agent-with-python-and-beautifulsoup/
# User Agent Strings obtained using https://www.whatismybrowser.com/
def GET_UA():
    uastrings = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0",
                 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
                 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44",
                 "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko",
                 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 OPR/70.0.3728.160",
                ]
    return random.choice(uastrings)

#converts relative links to absolute paths
# absolutePath code derived from
# https://stackoverflow.com/questions/476511/resolving-a-relative-url-path-to-its-absolute-path
def absolutePath(webpage, url):
    absoluteUrl = url
    if not url.startswith('http://www.'):
        absoluteUrl = requests.compat.urljoin(webpage, url)
    elif not url.startswith('https://www.'):
        absoluteUrl = requests.compat.urljoin(webpage, url)
    else:
        absoluteUrl = url
    return absoluteUrl

# code for handling system arguments
def checkForArguments():
    #code for argument handling
    try:
        webpage = sys.argv[1]
    except Exception as error:
        print("Error: A url is a required argument to find pdf links")
    return webpage

# gets response from http request or returns none
def validateRequest(url):
    headers = {'User-Agent': GET_UA()}
    response = None
    try:
        response = requests.get(url, headers=headers)
    except Exception as error:
        print("Unable to receive response from ", url)
        print("Try another webpage address")
    return response

def checkIfPDFRegEx(url):
    #use regex to check if link ends in .pdf
        m = re.search('.*(\.pdf)$', url) 
        # anything matches, then must be a pdf
        if m != None:
            return url
        return None
        
def printResults(response, link):
    print() # print a new line for aesthetics
    print("URI:", link) #link from anchor tag
    print("Final URI:", response.url) #obtained from response
    #check for content-length
    if 'Content-length' in response.headers:
        print("Content Length: {:,} bytes".format(int(response.headers['Content-length'])))    
    else:
        print('File Size Unknown')
    print() # print a new line for aesthetics

def main():
    webpage = checkForArguments()
    if webpage == '': return
    #get headers and text for url
    response = validateRequest(webpage)
    # parse response text using Beautiful soup to get links
    links = BeautifulSoup(response.text, 'html.parser').findAll('a')

    for link in links:
        #check if relative path and convert to absolute path
        url = absolutePath(webpage, link['href'])
        #check if pdf, and get http request
        url = checkIfPDFRegEx(url)
        if(url):
            response = validateRequest(url)
            if (response):
                #To account for bad links
                #Check once more if the final uri is a pdf
                if(checkIfPDFRegEx(response.url)):
                    response = validateRequest(response.url)
                    printResults(response, url)  

if __name__ == '__main__':
    main()