import urllib
from BeautifulSoup import *
import win_unicode_console 
win_unicode_console.enable()
import xml.etree.ElementTree as ET
import sqlite3
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


conn = sqlite3.connect('jobsie.sqlite')
cur = conn.cursor()
cur.executescript('''

CREATE TABLE IF NOT EXISTS Jobs ("Unique ID" TEXT UNIQUE, "Job Title" TEXT, "Job description" TEXT, Company TEXT, "Date added" TEXT, "Job Location" TEXT, Link TEXT)''')

new_jobs = 0
soupMail = BeautifulSoup(open('mail2.html'))
html = Tag(soupMail, "html")
table = Tag(soupMail, "table")
body = Tag(soupMail, "body")
tr = Tag(soupMail, "tr")
td = Tag(soupMail, "td")
soupMail.append(html)
html.append(body)
body.append(table)
table.append(tr)
table.attrs.append(("bgcolor", "purple"))
tr.append(td)

td.append('WE FOUND JOBBIES!')

td.attrs.append(('align', "center"))
td.attrs.append(('bgcolor', "NavajoWhite"))

tree = ET.parse('terms.xml')

for key in tree.findall('keyword'):
    key = key.text
    print 'Searching', key
    job_list = []
    if key == 'galway':
        url = 'http://www.jobs.ie/german-jobs-in-galway'
    else:
        url = 'http://www.jobs.ie/Jobs.aspx?regions=0&categories=0&keywords='+key+'&sort=Date&page=0&toPage=10&employerId=0%20+%20linkParams)'
    job_count = 0
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)

    jobs = soup.findAll('article', { 'class' : 'job-list-item' })
    for item in jobs:
        job_date = item.find('span', { 'class' : 'date'}).getText()
        job_long = item.find('span', { 'class' : 'snippet' })
        job_title = item.find('span', { 'class' : 'job' })
        job_company = item.find('span', { 'class' : 'name'})
        job_link = item.find('span', { 'class' : 'job' })
        job_location = item.find('span', { 'class' : 'location' })
        job_ID = item.find('span', { 'class' : 'shortlist_listing' })
        if job_date == 'Today':
            SQL_ID = job_ID.find('i').get('data-id')
            try:
                print 'Job title:', job_title.find('a').getText(), '@', job_company.find('a').getText()
                SQL_Title =  job_title.find('a').getText()
                SQL_Comp = job_company.find('a').getText()
            except: 
                print 'Job title: Undisclosed'
                SQL_Title =  'Undisclosed'
                print 'Company: Undisclosed'
                SQL_Comp = 'Undisclosed'
            try:
                print 'Job location:', job_location.getText()
                SQL_Loca = job_location.getText()
            except:
                print 'Job location: Undisclosed'
                SQL_Loca = 'Undisclosed'
            try:
                print 'Job link:', job_link.find('a').get('href')
                SQL_Link = job_link.find('a').get('href')
            except:
                print 'Job link: Unavailable'
                SQL_Link = 'Unavailable'
            try:
                print 'Job description:', job_long.find('a').getText(), '\n'
                SQL_Desc = job_long.find('a').getText()
            except:
                print 'Job description: Unavailable', '\n'
                SQL_Desc = 'Unavailable'
                job_list.append(SQL_Title + ' @ ' + SQL_Comp + '\n' + SQL_Desc + '\n' + SQL_Link + '\n' +  SQL_Loca).encode('ascii', 'ignore')
        
            job_count = job_count + 1
            SQL_Date = time.strftime("%c")

            job_full = [SQL_Title, SQL_Comp, SQL_Loca, SQL_Link]
                        
            try:
                cur.execute('''INSERT INTO Jobs ("Unique ID", "Job Title", Company, "Job description", Link, "Date added", "Job Location") 
                VALUES ( ?, ? , ? , ?, ?, ?, ?)''', (SQL_ID, SQL_Title, SQL_Comp, SQL_Desc, SQL_Link, SQL_Date, SQL_Loca ) )
                job_full = [SQL_Title, SQL_Comp, SQL_Loca, SQL_Link]
                td.append('<ul>')
                for attr in job_full:
                    td.append(attr)
                    td.append(' // ')
                td.append('</ul>')
                new_jobs = new_jobs + 1

            except: 
                continue   
    
        else:
            continue

mail_date = str(time.strftime("%x"))
addMailTitle = soupMail.findAll("title")
mail_count = str(new_jobs)
for tag in addMailTitle:
    tag.insert(0, NavigableString(mail_count + ' new jobs on ' + mail_date))
print(soupMail.prettify())
htmail = soupMail.prettify()
if new_jobs > 0:
    msg = MIMEMultipart()
    fromaddr = 'fromAddr'
    toaddr = 'toAddr'
    msg['From'] = 'fromAddr'
    msg['To']  = 'toAddr'
    msg['Subject'] = mail_count + ' new jobs on ' + mail_date
    msg.attach(MIMEText(htmail, 'html'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "fromAddrPW")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()   
conn.commit()

