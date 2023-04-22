from flask import Flask, render_template, url_for, request
import pymssql
import pandas as pd
import matplotlib.pyplot as plt
import os

# create a Flask app instance
app = Flask(__name__)


# set up the connection to Azure SQL Database
server = 'neeraj.database.windows.net'
database = 'kroger'
username = 'neeraj'
password = 'Cloud123!'

conn = pymssql.connect(server=server, user=username, password=password, database=database)
query = "SELECT * FROM [400_households]"
df_households = pd.read_sql(query, conn)
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



# generate the plot
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])
ax.set_title('My Plot')

# save the plot to a file
filename = 'myplot.png'
plt.savefig(filename)

# include the plot in your Flask template
@app.route('/plot')
def index():
    return render_template('index.html', plot_url=url_for('static', filename=filename))

@app.route('/', methods=['GET', 'POST'])
def search_results():
    if request.method == 'POST':
        # Get the search query from the form
        hshd_num = request.form['hshd_num']

        # Filter the dataframe based on the search query
        results = df_merged[df_merged['HSHD_NUM'] == int(hshd_num)].sort_values(['HSHD_NUM', 'BASKET_NUM', 'PURCHASE', 'PRODUCT_NUM', 'DEPARTMENT', 'COMMODITY'])

        # Convert the filtered dataframe to a list of dictionaries for rendering in HTML
        results_list = results.to_dict('records')
        
        

        # Render the search results on the same page
        return render_template('index.html', result=results_list)

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
