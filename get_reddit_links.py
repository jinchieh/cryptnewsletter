
# coding: utf-8

# In[146]:


#For beautifulsoup

from urllib2 import urlopen, Request
from bs4 import BeautifulSoup
import re
#For reddit keyword search:
import praw
import datetime
# In[147]:


import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#Dedupe links
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


# In[162]:


def scrape(link_list):
    reddit_urls = []

    for link in link_list:
        print(link)
        full_link = 'http://coinmarketcap.com' + link
        req = Request(full_link)
        response = urlopen(req)
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        alltext = soup.getText()

        #soup.findAll('TAGNAME', {'ATTR_NAME' :'ATTR_VALUE'})
        result = soup.findAll('script')
        result = str(result)

        #Match reddit link
        match = re.search(r'https://www.reddit.com/r/[A-Za-z0-9-_]*', result)
        if match:
            reddit_urls.append(match.group(0))
    print("All reddit links scraped.")

    return reddit_urls


# In[160]:

def collectnews(reddit, url_list, keyword, period):
    news = []
    for idx, url in enumerate(url_list):
        print(url)
        sr = reddit.subreddit(url)
        for i in sr.search(keyword, time_filter = period):
            news.append([url_list[idx], i.title.encode('utf-8'), get_date(i).isoformat(' '), i.url])
            print(url_list[idx], repr(i.title), get_date(i).isoformat(' '), i.url)
    print("...Done")
    return news

# def collectnews(df, user_idx, reddit, url_list, keyword, period):
#     news = []
#     for idx, url in enumerate(url_list):
#         print(url)
#         sr = reddit.subreddit(url)
#         for i in sr.search(keyword, time_filter = period):
#             news.append([df.loc[user_idx][idx+1], i.title.encode('utf-8'), get_date(i).isoformat(' '), i.url])
#             print(df.loc[user_idx][idx+1], repr(i.title), get_date(i).isoformat(' '), i.url)
#     print("...Done")
#     return news


# In[148]:


#Get date of reddit post
def get_date(submission):
    time = submission.created
    return datetime.datetime.fromtimestamp(time)


# In[173]:


def send_email(user, pwd, recipient, subject, body):
    import smtplib
    

    gmail_user = user
    gmail_pwd = pwd
    FROM = "Reddit Digest: "
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = ""
    if(type(body) == list):
        for row in body:
            TEXT = TEXT + str(row) + '\n'
    else:
        TEXT = body
        
    # # Prepare actual message
    # message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    # """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    # try:
    #     server = smtplib.SMTP("smtp.gmail.com", 587)
    #     server.ehlo()
    #     server.starttls()
    #     server.login(gmail_user, gmail_pwd)
    #     server.sendmail(FROM, TO, message)
    #     server.close()


    # Reference: https://docs.python.org/2/library/email-examples.html

    me = user
    you = recipient

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
    html = body

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, msg.as_string())
        server.close()



        print 'successfully sent the mail'
    except:
        print "failed to send mail"


