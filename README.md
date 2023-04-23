# azure-ml-kroger

CS6065 Final Project - Data Science with Azure on Kroger / 84.51 Data

API Endpoints
-------------
/data : Data Pull & Search by household

/analysis : Insights using Data Science

/upload : Upload New Data 

/login : Login

/logout : Logout


Questions Answered:
-----------------------
1. How does customer engagement change over time?
(a)What categories are growing or shrinking with changing customer engagement?
(b)
2. Which demographic factors (e.g. household size, presence of children, income) appear to affect customer engagement?
(a) Trends on demographics factors vs customer engagement
(b) How do they affect customer engagement with certain categories?
How might we re-engage customers within the store? Or within a specific category?

Technical Details:
------------------
1. Data is loaded on Azure SQL Database, cloud based SQL Server.
2. CSV Data loaded into Azure SQL using Azure Data Studio Import Wizard
3. Python Flask application connects to DB and queries tables before performing analysis
4. Deployed via gunicorn on Azure Virtual Machine

Manual Deployment Details:
-------------------------
0. Dependencies - pymssql, sqlalchemy, pandas, matplotlib, flask, gunicorn
1. Ensure DB connection is setup & firewall rules updated.

server = '<yourservername>.database.windows.net'
database = '<yourdbname>'
username = '<yourusername>'
password = '<yourpassword>'

2. export FLASK_APP = test.py
3. export FLASK_ENV = development
4. nohup python3 -m gunicorn test:app -b 0.0.0.0:5000 &
  
Adding New Data
---------------
 To load new data, use the Upload New Data link on the top of the page to open a page where you can upload the 3 csv files for households, transactions and products. Hit submit and it will redirect to the dashboard where you can see data pull from the new data. However, do not upload too much data with this method as it will cause timeout and crash the app. For very large volumes, use alternate method of inserting into the Azure SQL Database.
