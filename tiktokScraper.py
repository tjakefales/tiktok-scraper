#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 20:32:20 2021

@author: jakefales
"""

import selenium 
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
from selenium.common.exceptions import NoSuchElementException
import re
from datetime import date
from selenium.webdriver.common.action_chains import ActionChains
from random import seed
from random import random
from random import randint



opts = Options()
opts.add_argument("user-agent = Googlebot")
opts.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome("/Users/jakefales/Desktop/PythonLibraries/chromedriver 4", chrome_options=opts)

##Go to TikTok
driver.get("https://www.tiktok.com/")
time.sleep(5)

##----------------------------Initialize Lists -----------------------------------
usernameList = []
nameList = []
websiteList = []
emailList = []
linkedAccList = []
numberFollowersList = []
numberFollowingList = []
numberLikesList = []
mostRecentViewsList = []
avgViewsList = []



def search(tag): 
    driver.get("https://www.tiktok.com/tag/%s" %(tag))
    try:
        promotion = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.jsx-1437972206.promotion-expand.show" )))
        if len(promotion) != 0:
            closePromo = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.jsx-1437972206 > svg" )))
            closePromo.click()
    except: 
        None 
    


#----------------------------------Checking the dates --------------------------


def getDate():
    dateLine = WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.user-info-link.jsx-1229099585" )))
    chunks = dateLine[1].text.split("·")    
    dateFromChunk = chunks[1]
    
    if "ago" in dateFromChunk:
        return "recent"
    
    brokenDate = dateFromChunk.split("-") ##Split Date up by year, then month then day.
    if len(brokenDate) == 3:
        return date(int(brokenDate[0]), int(brokenDate[1]), int(brokenDate[2]))
    else:
        return date(2021, int(brokenDate[0]), int(brokenDate[1]))
    #print(brokenDate[0])
    
def checkDate():
   """
    Checks to see if the picture is within 6 months. 

    Parameters
    ----------
    picture : Date
        This is the date returned from getDate().

    Returns
    -------
    True if it is within six months (let's say 180 days).

    """
   today = date.today()
   if getDate() == "recent":
       return True
   elif 0 <= (today - getDate()).days  <= 180:
       return True 
   else:
       return False
   
 


#-------------------------------------Helper Functions ----------------------------

   
def convertToNum(elem):
    if "K" in elem.text:
        value = elem.text.split("K")[0]
        value = float(value)*1000
    elif "M" in elem.text:
        value = elem.text.split("M")[0]
        value = float(value)*1000000
    else:
        value = elem.text
        value = value.replace(",", "")
        value = int(value)
    
    return value   
    
   
def checkForError():
    errorPage = WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.jsx-3565499374.error-page" )))
    if len(errorPage) != 0:
        driver.refresh()

## Checks for popup and will close if there is one. 
def checkForPopup():
    popUp = WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.jsx-813273064.keyboard-shortcut-container" )))
    if len(popUp) > 1:
        closeButton = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.jsx-813273064.keyboard-shortcut-close" )))
        closeButton[1].click()

        return False
    else:
        return True

## We probably need to really increase this long wait time. 

def longRandomWait():
    timeToWait = randint(45, 90)
    time.sleep(timeToWait)
    print("waited %d seconds" %(timeToWait))
    
def medRandomWait():
    timeToWait = randint(20, 40) 
    time.sleep(timeToWait)
    print("waited %d seconds" %(timeToWait))
    
def shortRandomWait():
    timeToWait = randint(1, 5)
    time.sleep(timeToWait)
    #print("waited %d seconds" %(timeToWait))
    
   
#-----------------------------------Interacting with Bio/Header  ----------------------------

def getUsername(): 
    usernameChunk = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.share-title-container" )))
    username = usernameChunk.text.split('\n')[0]
    #print(username.text)
    return username

def getName():
    nameChunk = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.share-title-container" )))
    name = nameChunk.text.split('\n')[1]
    #print(username.text)
    return name


def getBio():
    bio =  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "h2.share-desc.mt10" )))
    #print(bio.text)
    return bio.text



def getEmail():
    """
    Gets any email from bio

    Returns
    -------
    email:
        Either nothing, a single email, or a list of all emails found in a bio.

    """
    bio = getBio()
    email = []
    chunks = bio.split()
    for chunk in chunks:
        if "@" in chunk and ".com" in chunk:
            #print(chunk)
            email.append(chunk)
    if len(email) == 0:
        return None
    elif len(email) == 1:
        return email[0]
    else:
        return email
    
def getWebsite():
    """
    Gets list of websites found in bios. Parses through the bio to find anything without @ but with .com as I assume
    all websites will have .com. This could also give links to social media (i.e. facebook.com)

    Returns
    -------
    website
        Either nothing, one website, or a list of websites.

    """
    
    website = []
    bio = getBio()
    chunks = bio.split()
    for chunk in chunks:
        if ".com" in chunk and not "@" in chunk:
            #print(chunk)
            website.append(chunk)
    if len(website) == 0:
        return None
    elif len(website) == 1:
        return website[0]
    else:
        return website
    
    
def getLinkedAccounts():
    """
    Get all accounts that are linked in a bio. This might not be their accounts on other social media,
    so this might require some checking over on the human side. This just returns anything in their "linked" or
    "shared" thing. 

    Returns
    -------
    acc: 
        This returns either nothing, a single linked account, or a list of all accounts in a bio.

    """
    acc = []
    try:
        accFromLinked = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.share-links" )))
        getOtherAccFromBio(acc)
        acc.append(accFromLinked.text)
        return acc.text
    except:
        getOtherAccFromBio(acc)
        return acc
    
def getOtherAccFromBio(acc):    
    bio = getBio()
    chunks = bio.split()
    for chunk in chunks:
        if "@" in chunk and not ".com" in chunk:
            #print(chunk)
            acc.append(chunk)
    if len(acc) == 0:
        return None
    elif len(acc) == 1:
        return acc[0]
    else:
        return acc

   
def getNumFollowers():
    numFollowers = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'strong[title = Followers]' )))
    
    # print(numFollowers.text)
    # print(convertToNum(numFollowers))
    return convertToNum(numFollowers)
        
def getNumFollowing():
    numFollowing = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'strong[title = Following]' )))
    
    
    # print(numFollowing.text)
    # print(convertToNum(numFollowing))
    return convertToNum(numFollowing)
    
def getNumLikes():
    numLikes = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'strong[title = Likes]' )))
    
    # print(numLikes.text)
    # print(convertToNum(numLikes))
    return convertToNum(numLikes)
     

    
#------------------------------Photo Information -------------------------------------

def getMostRecentViews():
    try:
        views = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "strong.jsx-2677948358.video-count" )))
    except:
        views = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "strong.jsx-26119655.video-count" )))
    
    # print(views.text)
    # print(convertToNum(views))
    return convertToNum(views)
    
    
    
    
def getAvgViews(numVids = 3):
    likes = 0
    try: 
        views = WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "strong.jsx-2677948358.video-count" )))
    except: 
        views = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "strong.jsx-26119655.video-count" )))

    for i in range(0, numVids):
        likes += convertToNum(views[i + 1])
        # print(likes)
    return likes / numVids
        
    
    
 #----------------------Putting it together ---------------------------------------   
    
def scrape(pagesToSearch, numPages, minFollowers = 100, minAvgViews = 100, numPostsForAvg = 3):
    ## Search for tag in list
    for page in pagesToSearch:
        ##Reset counters
        success = 0 
        pageCounter = 0   
        picIndex = 0
        waitCounter = 0
        
        search(page) ##Search page in list
        
        shortRandomWait()
          
        #photo = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.jsx-2261688415.video-feed-item.three-column-item" )))
        while success < numPages and pageCounter < 20: 
                        
            
            ##Every 5 photos (but not on multiples of 10s), have a medium random wait.
            if pageCounter % 10 == 5 :
                medRandomWait()
                
                
            ## Every 10 photos, have a long random wait, but make it have multiple as it goes further. 
            elif pageCounter % 10 == 0:
                waitCounter += 1
                for i in range(waitCounter):
                    if i < 3:
                        longRandomWait()
            ##Otherwise, just have a short random wait.           
            else: 
                shortRandomWait()
                print("short wait")
            
            try:
                photo = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.jsx-2261688415.video-feed-item.three-column-item" )))
            except:
                driver.refresh()
                checkForPopup()
                photo = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.jsx-2261688415.video-feed-item.three-column-item" )))

            time.sleep(1)
            photo[picIndex].click() #Click on post 
            print("Checking Page: ", pageCounter + 1)
            pageCounter += 1
            shortRandomWait()
            
            # Check the date and get the link to the user's page if date is within 6 months
            # and check username to make sure that it hasn't already been checked
            pageName = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.user-info-link.jsx-1229099585" )))
    
            if checkDate() == True and (pageName.text not in usernameList) :                                               
                link = pageName.get_attribute("href")
                
                # Open new tab, switch window to it, then open the user's page
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                shortRandomWait()
                driver.get(link)
                shortRandomWait()
               
                ## Check to see if followers and avg views meet parameters. 
                if (getNumFollowers() >= minFollowers and getAvgViews(numPostsForAvg) >= minAvgViews): 
                    getInfo(numPostsForAvg) ## Get the info
                    success += 1
                
                # Close the tab and switch back to the original window.
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                            
        
                shortRandomWait()
                    
            ##Close window 
            closeButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img.jsx-441496149.control-icon.close" )))
            closeButton.click()
                        
            
            picIndex += 1
        
        

    
    
    
    
def getInfo(numPostsForAvg = 3):
    '''
    Just puts together all of the helping functions to reduce typing in the scraping function.
    Adds all of their returns to the proper lists.
    
    Note: Average number of likes is set for the last 3 photos right now. I could make it a parameter, but 
    that might add some unneeded complexity for now.

    Returns
    -------
    None. But does add to the lists. 

    '''
    #print("Username: ", getUsername() ) 
    usernameList.append(getUsername())
    #print("Name: ", getName() ) 
    nameList.append(getName())
    #print("Bio: ", getBio() )
    #print("Website if any: ", getWebsite() )
    websiteList.append(getWebsite() )
    #print("email if any: ", getEmail() ) 
    emailList.append(getEmail())
    #print("Linked Accounts if any: ", getLinkedAccounts() )
    linkedAccList.append(getLinkedAccounts() )
    #print("Number of Followers: ", getNumFollowers() )
    numberFollowersList.append(getNumFollowers() )
    #print("Number of following: ", getNumFollowing() ) 
    numberFollowingList.append(getNumFollowing() )
    #print('Number of likes: ', getNumLikes())
    numberLikesList.append(getNumLikes() )
    #print("Likes on last photo: ", getMostRecentViews())
    mostRecentViewsList.append(getMostRecentViews())
    #print("Avg likes on last 3 photos: ", getAvgViews(numPostsForAvg))
    avgViewsList.append(getAvgViews(numPostsForAvg))
    
    

def storeData(title):
    '''
    Exports the data from the scrape into a CSV file (should be able to be opened up by Excel, Sheets, or SQL)
    Note for Options: Could be added to the end of the scrape function so it automatically exports at the end.
    Downside to that is if you wanted to make multiple searches all in one list, then you'd have multiple
    documents. 
    Other Note: It currently does not clear the data after exporting. Use resetLists() after this to reset,
    or I can just implement it into the function overall. '

    Parameters
    ----------
    title : string
        Give the title of the spreadsheet to export. Must be in quotations and end with csv.
        Can find the file in whatever your working directory is (I'll figure this out in relation to the server)
                                                                 
        Example: storeData('example.csv')

    Returns
    -------
    None.

    '''
    df = pd.DataFrame({'Username':usernameList,'Name':nameList,'Website':websiteList, 'email':emailList,
                       'linked accounts':linkedAccList,'Number of Followers':numberFollowersList,
                       'Number of following':numberFollowingList, 'Number of total likes': numberLikesList,
                       'Views on last post': mostRecentViewsList,
                       'Avg Views':avgViewsList})
    df.to_csv(title, index=False, encoding='utf-8')   
    
    resetLists()
    
    
    
def resetLists():
    usernameList.clear()
    nameList.clear()
    websiteList.clear()
    emailList.clear()
    linkedAccList.clear()
    numberFollowersList.clear()
    numberFollowingList.clear()
    numberLikesList.clear()
    mostRecentViewsList.clear()
    avgViewsList.clear()
    

    
    