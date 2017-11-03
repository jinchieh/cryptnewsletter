
# coding: utf-8

# In[78]:


import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import praw

import datetime
import time
from get_reddit_links import f7, scrape, collectnews, send_email
from retrieve_html import retrieve_html

from urllib2 import urlopen, Request
from bs4 import BeautifulSoup


import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from retrieve_html import retrieve_html

from string import Template
import tldextract

from apscheduler.scheduler import Scheduler
import logging
logging.basicConfig()

import datetime
import requests
# In[ ]:


#Before ap_scheduler

global email_list

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('bitcoin railroad-8cc9cd351748.json', scope)
client = gspread.authorize(creds)
 
# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("bitcoin railroad registration").sheet1

# In[21]:


list_of_lists = sheet.get_all_values()
df = pd.DataFrame(list_of_lists[1:])
df = df[[2]]
df.columns = ['email']
df = df[df.email != ""]


email_list = []
for email in df['email']:
    email_list.append(email)


# In[2]:

# Start the scheduler
sched = Scheduler()
sched.daemonic = False
sched.start()

def minute_price_historical(symbol, comparison_symbol, limit, aggregate, exchange=''):
    url = 'https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym={}&limit={}&aggregate={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
    if exchange:
        url += '&e={}'.format(exchange)
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df

def daily_price_historical(symbol, comparison_symbol, limit=1, aggregate=1, exchange='', allData='true'):
    url = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&limit={}&aggregate={}&allData={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate, allData)
    if exchange:
        url += '&e={}'.format(exchange)
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df



def job_function():
    print("Hello World")
    print(datetime.datetime.now())

     
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('bitcoin railroad-8cc9cd351748.json', scope)
    client = gspread.authorize(creds)
     
    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("bitcoin railroad registration").sheet1

    # In[21]:


    list_of_lists = sheet.get_all_values()
    df = pd.DataFrame(list_of_lists[1:])
    df = df[[2,4,5,6,7,8,9,10,11,12,13]]
    df.columns = ['email', 'coin1','coin2', 'coin3', 'coin4', 'coin5', 'url1', 'url2', 'url3', 'url4', 'url5']
    df = df[df.email != ""]


    # In[8]:

## FILL THIS IN:

    client_id = ""
    client_secret = ""
    username = ""
    password = ""
    user_agent = ""


    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, password=password, username=username,user_agent=user_agent)
    
    keywords = ["release", "listing", "partnership", "campaign", "conference", "rumor", "china", "korea", "japan", "government"]

    


    # In[115]:





    # In[120]:


    now_hour = datetime.datetime.now().hour
    now_minute = datetime.datetime.now().minute


    # In[ ]:

# FOR NEW SUBSCRIBERS

    # for idx, row in df.iterrows():
        
    #     email = df.loc[idx][0]
    #     if email not in email_list:

    #         print(email)

    #         tokens = []
    #         for i in (0,1,2,3,4):
    #             tokens.append(df.loc[idx][i+1])

    #         price_texts = []

    #         for token in tokens:
    #             print(tokens)
    #             print(token)
    #             price_time = minute_price_historical(token, 'BTC', 1, 1).iloc[-1]['timestamp']
    #             close = minute_price_historical(token, 'BTC', 1, 1).iloc[-1]['close']
    #             time_text = price_time.strftime("%H:%M") + " EST"
    #             high30 = daily_price_historical(token, 'BTC', 1, 1)[-31:-1]['high'].max()
    #             low30 = daily_price_historical(token, 'BTC', 1, 1)[-31:-1]['low'].min()

    #             price_text = "<h2>$" + str(token) + ": " + str(close) + " sats (" + str(time_text) + ") </h2> <h3>30-day high (low): " + str(high30) + " (" + str(low30) + ") sats</h3><br>"

    #             print(price_text)

    #             price_texts.append(price_text)


    #         prices = ''.join(price_texts)
    #         print(prices)

    #         reddit_urls = []
    #         reddit_urls.append(df.loc[idx][6][25:])
    #         reddit_urls.append(df.loc[idx][7][25:])
    #         reddit_urls.append(df.loc[idx][8][25:])
    #         reddit_urls.append(df.loc[idx][9][25:])
    #         reddit_urls.append(df.loc[idx][10][25:])

    #         news_all = []


    #         #print(df.loc[idx][idx2+1])
    #         for keyword in keywords:
    #             print("Searching for  " + keyword + "...")
    #             news = collectnews(reddit, reddit_urls, keyword = keyword, period = "day")
    #             #for item in news:
    #                 #item[0] = df.loc[idx][idx2+1]
    #             #print(df.loc[idx+1])
    #             print(news)
    #             news_all = news_all + news

    #             print("All News: ", news_all)

    #         no_news_toggle = False
    #         if news_all == [] or len(news_all) < 5:
    #             no_news_toggle = True
    #             print("No news found. Searching in bitcoin and ethereum...")
    #             reddit_urls = []
    #             reddit_urls.append("bitcoin")
    #             reddit_urls.append("ethereum")

    #             for keyword in keywords:
    #                 print("Searching for  " + keyword + "...")
    #                 news = collectnews(reddit, reddit_urls, keyword = keyword, period = "hour")
    #                 #for item in news:
    #                     #item[0] = df.loc[idx][idx2+1]
    #                 #print(df.loc[idx+1])
    #                 print(news)
    #                 news_all = news_all + news


    #         #news_all = dict((x[3], x) for x in news_all).values()
    #         news_all = sorted(news_all)


    #         #select coin/reddit for first instance to set as title
    #         search = news_all[0][0]
    #         for news in news_all[1:]:
    #            if news[0] == search:
    #                news[0] = ""
    #            else: 
    #                search = news[0]






    #         news_all_lines = []
    #         for news in news_all:
    #             extracted = tldextract.extract(news[3])
    #             domain = "{}.{}".format(extracted.domain, extracted.suffix)
               
    #             news_all_lines.append("""<br><h2><div align="center">""" + str(news[0]).upper() + "</div></h2> [" + domain.capitalize() + """] <a href=" """ + str(news[3]) + """ ">""" + str(news[1]) + "</a>")
            
    #             news_all_final = ' '.join([news_line for news_line in news_all_lines])
    #         # In[171]:
    #         if no_news_toggle == True:
    #             no_news = "<br><h3> Check back tomorrow for more news on your favorite coins. In the meantime, check out these news in bitcoin/ethereum below! </h3><br>"
    #         else:
    #             no_news = ""


                # FILL THIS IN:

               # user = "" #Email to send from
              #  pwd = "" #Password of email to send from
              #  recipient = "" # Receiving email



    #         body = retrieve_html()
    #         msg = Template(body).safe_substitute(comment = news_all_final, price = prices, no_news = no_news)


    #         # now = datetime.datetime.now()
    #         # if now.hour > 12:
    #         #     subject = str(now.month) + "/" + str(now.day) + " Reddit News " + str(now.hour - 12) + "pm"
    #         # else:
    #         #     subject = str(now.month) + "/" + str(now.day) + " Reddit News " + str(now.hour) + "am"  

    #         now = datetime.datetime.now()
    #         nowhour = str(now.month)

    #         d0 = datetime.date(2017, 10, 25)
    #         d1 = datetime.date.today()
    #         delta = d1 - d0

    #         subject = "Bitcoin Railroad: Train #" + str(delta.days) 

    #         if msg:
    #             send_email(user, pwd, recipient, subject, msg)


    #         part = MIMEText(body, 'html')


    #         print("end")

    #         email_list.append(email)

    # In[92]:


    if (now_hour == 7 and now_minute == 0):

        for idx, row in df.iterrows():

            try:

                #Retrieve token symbols
                tokens = []
                for i in (0,1,2,3,4):
                    tokens.append(df.loc[idx][i+1])

                price_texts = []

                for token in tokens:
                    print(tokens)
                    print(token)
                    price_time = minute_price_historical(token, 'BTC', 1, 1).iloc[-1]['timestamp']
                    close = minute_price_historical(token, 'BTC', 1, 1).iloc[-1]['close']
                    time_text = price_time.strftime("%H:%M") + " EST"
                    high30 = daily_price_historical(token, 'BTC', 1, 1)[-31:-1]['high'].max()
                    low30 = daily_price_historical(token, 'BTC', 1, 1)[-31:-1]['low'].min()

                    price_text = "<h2>$" + str(token) + ": " + str(close) + " sats (" + str(time_text) + ") </h2> <h3>30-day high (low): " + str(high30) + " (" + str(low30) + ") sats</h3><br>"

                    print(price_text)

                    price_texts.append(price_text)


                prices = ''.join(price_texts)
                print(prices)

                reddit_urls = []
                reddit_urls.append(df.loc[idx][6][25:])
                reddit_urls.append(df.loc[idx][7][25:])
                reddit_urls.append(df.loc[idx][8][25:])
                reddit_urls.append(df.loc[idx][9][25:])
                reddit_urls.append(df.loc[idx][10][25:])

                news_all = []


                #print(df.loc[idx][idx2+1])
                for keyword in keywords:
                    print("Searching for  " + keyword + "...")
                    news = collectnews(reddit, reddit_urls, keyword = keyword, period = "day")
                    #for item in news:
                        #item[0] = df.loc[idx][idx2+1]
                    #print(df.loc[idx+1])
                    print(news)
                    news_all = news_all + news

                    print("All News: ", news_all)

                no_news_toggle = False
                if news_all == [] or len(news_all) < 5:
                    no_news_toggle = True
                    print("No news found. Searching in bitcoin and ethereum...")
                    reddit_urls = []
                    reddit_urls.append("bitcoin")
                    reddit_urls.append("ethereum")

                    for keyword in keywords:
                        print("Searching for  " + keyword + "...")
                        news = collectnews(reddit, reddit_urls, keyword = keyword, period = "hour")
                        #for item in news:
                            #item[0] = df.loc[idx][idx2+1]
                        #print(df.loc[idx+1])
                        print(news)
                        news_all = news_all + news


                #news_all = dict((x[3], x) for x in news_all).values()
                news_all = sorted(news_all)


                #select coin/reddit for first instance to set as title
                search = news_all[0][0]
                for news in news_all[1:]:
                   if news[0] == search:
                       news[0] = ""
                   else: 
                       search = news[0]






                news_all_lines = []
                for news in news_all:
                    extracted = tldextract.extract(news[3])
                    domain = "{}.{}".format(extracted.domain, extracted.suffix)
                    news_all_lines.append("""<br><h2><div align="center">""" + str(news[0]).upper() + "</div></h2> [" + domain.capitalize() + """] <a href=" """ + str(news[3]) + """ ">""" + str(news[1]) + "</a>")

                    news_all_final = ' '.join([news_line for news_line in news_all_lines])
                # In[171]:

                if no_news_toggle == True:
                    no_news = "<br><h3> Check back tomorrow for more news on your favorite coins. In the meantime, check out these news in bitcoin/ethereum below! </h3><br>"
                else:
                    no_news = ""

                # FILL THIS IN:

                user = "" #Email to send from
                pwd = "" #Password of email to send from
                recipient = "" # Receiving email



                body = retrieve_html()
                msg = Template(body).safe_substitute(comment = news_all_final, price = prices, no_news = no_news)


                # now = datetime.datetime.now()
                # if now.hour > 12:
                #     subject = str(now.month) + "/" + str(now.day) + " Reddit News " + str(now.hour - 12) + "pm"
                # else:
                #     subject = str(now.month) + "/" + str(now.day) + " Reddit News " + str(now.hour) + "am"  

                now = datetime.datetime.now()
                nowhour = str(now.month)

                d0 = datetime.date(2017, 10, 25)
                d1 = datetime.date.today()
                delta = d1 - d0

                subject = "Bitcoin Railroad: Train #" + str(delta.days) 

                if msg:
                    send_email(user, pwd, recipient, subject, msg)


                part = MIMEText(body, 'html')


                print("end")

            except Exception, e:
                print(e) 
                pass
        


    
    time.sleep(20)

# Schedules job_function to be run once each minute
sched.add_cron_job(job_function,  minute='0-59', misfire_grace_time = 1200)

