#!/usr/bin/python3

import argparse
from bs4 import BeautifulSoup
import re
import requests, json
import sys
import time
import urllib.request
from urllib.parse import urlparse

###  Objectives
# [x] 1  - take input URL
# [x] 2   > find all .js files and list their URL in an array || download
# [x] 2a         (search for tag opener starting "<script" and containing "src=")
# [x] 2b         if it does not begin with "https://", treat it as local and append targ domain"
# [ ] 2.1           - may want to have some level of validation + error reporting, to identify if
#                     any number of items were not pulled successfully after setting to local dom
# [ ] 3    + review for specific items:
#           :: keys, 'admin', software/versions, private IPs, URLs,
#           :: decoding mechanisms, etc.
#########################################

parser = argparse.ArgumentParser(description='URL script scraper..\nSearch scripts on a given URL for items of interest.')
parser.add_argument('-u', type=str, required=False, help='set target URL')
args = parser.parse_args()
targURL = args.u

#  1  #
while targURL == '':
  try:
    targURL = input("Target URL: ")
    validTarg = input("\033[A                                                                                                                                                                                                    \033[A\033[32mTARGET\033[0m:  \033[3m\033[4m" + targURL + "\033[0m" + "\nCorrect?  ")
    if "y" in validTarg.lower():
      pass
      print("\033[A                                                                                                                                                                                                    \033[A")
    else:
      print("\033[A                                                                                                                                                                                                    \033[A \033[31mtry again...\033[0m")
      time.sleep(1)
      print("\033[A                                                                                                                                                                                                    \033[A")
      continue
  except:
    print(" : Invalid input.")
    continue
  else:
    break

domain = urlparse(targURL).netloc
if "https" in targURL:
  protocol = "https://"
elif "http" in targURL:
  protocol = "http://"
else:
  protocol = "https://"

#  2  #
soup = BeautifulSoup(requests.get(targURL).content, 'html.parser')
soup2 = BeautifulSoup(requests.get(targURL).text, 'html.parser')  # does this still need to be here?

internalScript = soup2.find_all('script')
internal_js = list(filter(lambda script: not script.has_attr("src"), internalScript))

urls = []
for link in soup.find_all('script'):
  toStr = str(link.get('src'))
  if "none" in toStr.lower():
    pass
  else:
    urls.append(toStr)

#  2a, 2b  #

localScripts = []
extScripts = []

def sortScripts():
  for u in urls:
    if domain in u:
      localScripts.append(u)
    elif "http" not in u:
      localScripts.append(u)
    else:
      extScripts.append(u)

def printAllScripts():
  print('\n'.join(urls))

def printLocal():
  print('\033[1m\033[3mLocal server scripts: \033[0m')
  print('\n'.join(localScripts))

def printExt():
  print('\033[1m\033[3mExternally-hosted scripts: \033[0m')
  print('\n'.join(extScripts))

def printInt():
  print('\033[1m\033[3mInternal page scripts: \033[0m')
  print(internal_js)

fullLocalURLs = []
def makeFullLocalURL():
  for file in localScripts:
    fullURL = protocol + domain + "/" + file
    fullLocalURLs.append(fullURL)

#  3  #
possibleFinding = []
def testScriptSearch():
  global match
  match = 0
  print()
  print("TESTING LOCAL SCRIPT SEARCH...")
  print("..............................")
  for f in fullLocalURLs:
    print()
    print("\033[4m"+f+"\033[0m:")
    try:
      r = requests.get(f)
      if r.ok:
        text = r.text
    except requests.exceptions.ConnectionError as exc:
      print(exc)

    patterns = ['admin', 'captureDocumentDownload', 'capturePageVisit', 'PseudO']
    for pattern in patterns:
      if re.search(pattern, text, re.IGNORECASE):
        print('* MATCH!  ' + '\033[32m' + pattern + '\033[0m  \033[3mfound in:  \033[0m\033[4m' + f + '\033[0m')
        match += 1
    exit()

def matchCount():
  print('Total match count:  ' + str(match))

################
#     MAIN     #

sortScripts()
printLocal()
print()
printExt()
print()
printInt()
print()
makeFullLocalURL()
testScriptSearch()
matchCount()
