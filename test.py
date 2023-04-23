from flask import Flask, render_template, url_for, request, redirect, flash, session
import pymssql
import pandas as pd
import os, io, base64, plot, pymssql, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pyodbc
from sqlalchemy import create_engine, MetaData


app = Flask(__name__)
app.config['SECRET_KEY'] = "thisisasecret!!!!"

server = 'neeraj.database.windows.net'
database = 'kroger'
username = 'neeraj'
password = 'Cloud123!'

print("hello")
conn = pymssql.connect(server=server, user=username, password=password, database=database)
#conn2 = 'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={0};DATABASE={1};UID={2};PWD={3}'.format(server, database, username, password)
#conn2 = pyodbc.connect(conn2)
#engine = create_engine(f'mssql+pymssql://{username}:{password}@{server}/{database}')
engine = create_engine('mssql+pymssql://{}:{}@{}/{}'.format(username, password, server, database))

metadata = MetaData()
metadata.reflect(bind=engine)
metadata.bind = engine

conn = engine
print("connected")
query = "SELECT * FROM [400_households]"
df_households = pd.read_sql(query, conn)
print("done")
query = "SELECT * FROM [400_transactions]"
df_transactions = pd.read_sql(query, conn)
query = "SELECT * FROM [400_products]"
df_products = pd.read_sql(query, conn)
print(df_products[:5])
print(df_households.shape)
print(df_transactions.shape)
print(df_products.shape)
df_merged = pd.merge(df_transactions, df_products, on='PRODUCT_NUM')
df_merged = pd.merge(df_merged, df_households, on='HSHD_NUM')
df_merged = df_merged.sort_values(['HSHD_NUM', 'BASKET_NUM', 'PURCHASE', 'PRODUCT_NUM', 'DEPARTMENT', 'COMMODITY'])

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Load CSV files into pandas dataframes
        df_h = pd.read_csv(request.files['file1'])
        df_t = pd.read_csv(request.files['file2'])
        df_p = pd.read_csv(request.files['file3'])
        
        print(df_h.shape)
        # Do something with the dataframes, e.g. merge them, perform analysis, etc.

        return 'Files uploaded successfully!'
    
    # Render the upload.html template for GET requests
    return render_template('upload.html')



@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route('/login',methods=['GET','POST'])
def login():
  if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        if name == password:
            flash('You were successfully logged in!')
            session['username'] = name
            return redirect(url_for('data'))
        else:
            flash("Incorrect password. Hint: Username and password are same..")
        
        return render_template('login.html')
  elif request.method == 'GET':
    return render_template('login.html')

# Testing
@app.route('/plot')
def index():
    return render_template('index.html', plot_url=url_for('static', filename=filename))
# Insights View
@app.route('/analysis')
def analysis():
    if request.method=="GET":
        temp = df_merged
        plot_data1 = plot.total_spend_department(temp)
        plot_data2 = plot.percent_change_department(temp)
        plot_data3 = plot.distribution_spend_department(temp)
        
        # QUESTION 1 A
        plot_data4 = plot.department_per_week(temp)
        df = df_merged
        df_food = df[df['DEPARTMENT'].str.strip() == 'FOOD']
        print(df_food.shape)
        plot_data5 = plot.commodity_per_week(df_food)
        df_nonfood = df[df['DEPARTMENT'].str.strip() == 'NON-FOOD']
        print(df_nonfood.shape)
        plot_data6 = plot.commodity_per_week(df_nonfood)
        df_pharma = df[df['DEPARTMENT'].str.strip() == 'PHARMA']
        print(df_pharma.shape)
        plot_data7 = plot.commodity_per_week(df_pharma)
        
        #QUESTION 1 B
        plot_data8 = plot.spend_all_households(temp)
        plot_data9 = plot.spend_range_households(temp)
        plot_data10 = plot.weekly_spend_per_household(temp)
        plot_data11 = plot.total_spend_per_week(temp)
        
        #QUESTION 2 A
        plot_data12 = plot.hh_size_engagement(temp)
        plot_data13 = plot.children_engagement(temp)
        plot_data14 = plot.income_engagement(temp)
        
        #QUESTION 2 B
        plot_data15 = plot.hhsize_department(temp)
        plot_data16 = plot.children_department(temp)
        plot_data17 = plot.income_department(temp)

        
    return render_template('analysis.html', result=None,plot_data1=plot_data1
                           ,plot_data2=plot_data2
                           ,plot_data3=plot_data3
                           ,plot_data4=plot_data4
                           ,plot_data5=plot_data5
                           ,plot_data6=plot_data6
                           ,plot_data7=plot_data7
                           ,plot_data8=plot_data8
                           ,plot_data9=plot_data9
                           ,plot_data10=plot_data10
                           ,plot_data11=plot_data11
                           ,plot_data12=plot_data12
                           ,plot_data13=plot_data13
                           ,plot_data14=plot_data14
                           ,plot_data15=plot_data15
                           ,plot_data16=plot_data16
                           ,plot_data17=plot_data17)
            
@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        # Get the search query from the form
        hshd_num = request.form['hshd_num']

        # Filter the dataframe based on the search query
        results = df_merged[df_merged['HSHD_NUM'] == int(hshd_num)].sort_values(['HSHD_NUM', 'BASKET_NUM', 'PURCHASE', 'PRODUCT_NUM', 'DEPARTMENT', 'COMMODITY'])

        # Create figure with 3 subplots
        fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(10, 15))

        # Create pie chart of department percentages
        df_dept = results.groupby('DEPARTMENT').size().reset_index(name='counts')
        ax[0].pie(df_dept['counts'], labels=df_dept['DEPARTMENT'], autopct='%1.1f%%')
        ax[0].set_title('Department Percentages')

        # pie chart showing percentage of product commodities
        df_commodity = results.groupby('COMMODITY').size()
        ax[1].pie(df_commodity.values, labels=df_commodity.index, autopct='%1.1f%%')
        ax[1].set_title('Product Commodities Purchased')

        # Create line plot of spend per week
        #df_weeks = results.groupby('WEEK_NUM')['SPEND'].sum().reset_index(name='total_spend')
        #df_weeks['SPEND_PER_WEEK'] = df_weeks['total_spend'] / df_weeks['WEEK_NUM']
        df_weekly_spend = results.groupby('WEEK_NUM')['SPEND'].sum()

        ax[2].plot(df_weekly_spend.index, df_weekly_spend.values, marker='o')
        ax[2].set_xlabel('Week')
        ax[2].set_ylabel('Total Spend $')
        ax[2].set_title('Spend per Week Over Time')


        # Convert the plot to a PNG image
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        plot_data = base64.b64encode(buf.getvalue()).decode('ascii')

    
        # Convert the filtered dataframe to a list of dictionaries for rendering in HTML
        results_list = results.to_dict('records')
        
        

        # Render the search results on the same page
        return render_template('index.html', result=results_list,plot_data=plot_data)

    elif request.method == 'GET':
        # Render the search form, and also top 5000 results 
        results = df_merged[:1000].sort_values(['HSHD_NUM', 'BASKET_NUM', 'PURCHASE', 'PRODUCT_NUM', 'DEPARTMENT', 'COMMODITY'])
        return render_template('index.html', result=results.to_dict('records'))

        
    # Render the search form
    return render_template('index.html')

# define a route and function to query the database
@app.route('/query_db')
def query_db():
    #query = "SELECT * FROM [400_households]"

    #df = pd.read_sql(query, conn)
    
    return df_merged[:10].to_html()

# run the Flask app
if __name__ == '__main__':
    app.run()
