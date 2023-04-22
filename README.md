# azure-ml-kroger

CS6065 Final Project - Data Science with Azure on Kroger / 84.51 Data

API Endpoints
-------------
/data : Data Pull & Search by household

/analysis : Insights using Data Science

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

Writeup:
How might we re-engage customers within the store? Or within a specific category?

Technical Details:
------------------
1. Data is loaded on Azure SQL Database, cloud based SQL Server.
2. CSV Data loaded into Azure SQL using Azure Data Studio Import Wizard
3. Python Flask application connects to DB and gathers insights
4. Deployed on Azure App Engine

Manual Deployment Details:
-------------------------
1. Ensure DB connection is setup.

server = '<yourservername>.database.windows.net'
database = '<yourdbname>'
username = '<yourusername>'
password = '<yourpassword>'

3. export FLASK_APP = test.py
4. export FLASK_ENV = development
5. flask run
  
Adding New Data
---------------
  There are two options:
  (a) connect to my SQL Server DB and use Azure Data Studio to import new csv or SQL queries to add new data
  (b) Upload new data directly into the application, will be processed with pandas
