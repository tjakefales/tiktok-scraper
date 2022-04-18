# tiktok-scraper
Uses Python Selenium to get simple public information on different metrics on an account. Note that css selectors need regularly updated.


This project provides a way to theoretically automate a process of getting simple public information on different
tiktok accounts (i.e. number of followers or average views). 

Please be aware of TikTok community guidelines as they relate to using bots on their website and use this code at your own risk. 


## General Directions: 
-- Make sure to have a Google ChromeDriver saved in working directory.  

-- Run program to bring up automated Window that goes straight to tiktok. 

-- Use the scrape method with following parameters: 
  -- pagesToSearch = array of the different tags to search
  -- numPages = int number of accounts to look at for each tag
  -- minFollowers = int minimum number of followers for account to be looked at (default 100)
  -- minAvgViews = int minimum number of average views for account to be looked at (default 100)
  -- numPostsForAvg = int number of posts to take the average number of views per post (default 3)

-- After scrape finishes running, use storeData method to export as .csv. 

## Future Updates / things to work on: 
-- Scrape method (among other methods) needs refactoring

-- connection to relational database (mySql?)

-- Use Django to help integrate a front end 
  

