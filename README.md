"# jobtown" 
Job scraper for jobs.ie

This is a simple mail notification system for jobs on jobs.ie.

I was tired of their search and notification system so I wrote a script that automatically does all that for me.

terms.xml: add all search terms you are interested in as new keywords

mail2.html: this file is populated with results from the search

jobsie.sqlite: here all jobs are stored and the script checks this database to determine if the job is new or has been found before

Not sure how to add BeautifulSoup to it, however if you put all files in one folder, it should work.

To use the mail notification system, add your details to the code or comment the mailing part out if you are only interested in the database.

The mail is currently only working when using gmail. You may have to change your gmail settings to allow this application.
