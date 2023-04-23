import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

import seaborn as sns

def encode(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plot_data = base64.b64encode(buf.getvalue()).decode('ascii')
    return plot_data
    
def total_spend_department(temp):
    df = temp.copy()
    df['PURCHASE'] = pd.to_datetime(df['PURCHASE'])
    df.set_index('PURCHASE', inplace=True)
    df_resampled = df.groupby(['DEPARTMENT', pd.Grouper(freq='W')])['SPEND'].sum().reset_index()
    df_pivot = df_resampled.pivot(index='PURCHASE', columns='DEPARTMENT', values='SPEND')
    df_total_spend = df_resampled.groupby('DEPARTMENT')['SPEND'].sum()
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_title('Total Spend by Department')
    ax.set_ylabel('Total Spend')
    ax.bar(df_total_spend.index, df_total_spend.values)
    for i, val in enumerate(df_total_spend.values):
        ax.text(i, val, df_total_spend.index[i], ha='center')
    return encode(fig)



def percent_change_department(temp):
    data = temp.copy()
    dept_grouped = data.groupby(['DEPARTMENT', 'YEAR'])['SPEND'].sum().reset_index()
    dept_pivot = dept_grouped.pivot(index=['YEAR'], columns='DEPARTMENT', values='SPEND')
    dept_pct_change = dept_pivot.pct_change().fillna(0)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(dept_pct_change, cmap='coolwarm', center=0, annot=True, fmt='.0%', cbar_kws={'label': 'Percent Change'})
    ax.set_title('Yearly Percent Change in Spend by Department')
    ax.set_ylabel('Year')
    ax.set_xlabel('Department')
    return encode(fig)


def distribution_spend_department(temp):
    df = temp.copy()
    weekly_dept_commodity_spend = df.groupby(['WEEK_NUM', 'DEPARTMENT', 'COMMODITY'])['SPEND'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(12, 6))

    for dept in weekly_dept_commodity_spend['DEPARTMENT'].unique():
        dept_data = weekly_dept_commodity_spend[weekly_dept_commodity_spend['DEPARTMENT'] == dept]
        ax.hist(dept_data['SPEND'], bins=20, alpha=0.5, label=dept)

    # Add axis labels and legend
    ax.set_xlabel('Spend')
    ax.set_ylabel('Frequency')
    ax.set_title('Distribution of Spend per Category by Week')
    ax.legend()
    
    return encode(fig)

# QUESTION 1 A - CHANGING CUSTOMER ENGAGEMENT OVER TIME
def department_per_week(temp):
    df = temp.copy()
    spend_per_week_dep = df.groupby(['WEEK_NUM', 'DEPARTMENT'])['SPEND'].sum().reset_index()

    # Plot spend per department over all the weeks
    fig, ax = plt.subplots(figsize=(12, 6))
    for dep in spend_per_week_dep['DEPARTMENT'].unique():
        dep_data = spend_per_week_dep[spend_per_week_dep['DEPARTMENT'] == dep]
        ax.plot(dep_data['WEEK_NUM'], dep_data['SPEND'], label=dep)
    ax.set_title('Total Spending per Department per Week')
    ax.set_xlabel('Week')
    ax.set_ylabel('Total Spend')
    ax.legend()
    return encode(fig)

def commodity_per_week(temp):
    df = temp.copy()
    spend_per_week_dep = df.groupby(['WEEK_NUM', 'COMMODITY'])['SPEND'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(12, 10))
    for dep in spend_per_week_dep['COMMODITY'].unique():
        dep_data = spend_per_week_dep[spend_per_week_dep['COMMODITY'] == dep]
        ax.plot(dep_data['WEEK_NUM'], dep_data['SPEND'], label=dep)
    ax.set_title('Total Spending per COMMODITY per Week')
    ax.set_xlabel('Week')
    ax.set_ylabel('Total Spend')
    ax.legend()
    return encode(fig)

# QUESTION 1 B - HOUSEHOLD EXPENDITURE DYNAMICS

def spend_all_households(temp):
    df = temp.copy()
    df_hh_week = df.groupby([pd.Grouper(key='WEEK_NUM'), pd.Grouper(key='HSHD_NUM')])['SPEND'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(12, 8))
    for key, grp in df_hh_week.groupby(['HSHD_NUM']):
        ax = grp.plot(ax=ax, kind='line', x='WEEK_NUM', y='SPEND', label=key)
    ax.set_xlabel('Week Number')
    ax.set_ylabel('Total Spend')
    ax.set_title('Total Spend per Household per Week')
    return encode(fig)

def spend_range_households(temp):
    df = temp.copy()
    df_hh_week = df.groupby([pd.Grouper(key='WEEK_NUM'), pd.Grouper(key='HSHD_NUM')])['SPEND'].sum().reset_index()
    df_hh_spend = df_hh_week.groupby('HSHD_NUM')['SPEND'].sum().reset_index()
    df_hh_spend = df_hh_spend.sort_values('SPEND')
    fig, ax = plt.subplots(figsize=(12, 8))

    # plot households with lowest spend
    for i, row in df_hh_spend.head(5).iterrows():
        df_plot = df_hh_week[df_hh_week['HSHD_NUM']==row['HSHD_NUM']]
        ax.plot(df_plot['WEEK_NUM'], df_plot['SPEND'], label=row['HSHD_NUM'])

    # plot households with highest spend
    for i, row in df_hh_spend.tail(5).iterrows():
        df_plot = df_hh_week[df_hh_week['HSHD_NUM']==row['HSHD_NUM']]
        ax.plot(df_plot['WEEK_NUM'], df_plot['SPEND'], label=row['HSHD_NUM'])
        
    ax.set_xlabel('Week Number')
    ax.set_ylabel('Total Spend')
    ax.set_title('Total Spend per Household per Week')
    ax.legend(title='Household Number')
    return encode(fig)

def weekly_spend_per_household(temp):
    df = temp.copy()
    # group by household and week, summing up the spend
    df_hh_week = df.groupby([pd.Grouper(key='WEEK_NUM'), pd.Grouper(key='HSHD_NUM')])['SPEND'].sum().reset_index()

    # calculate average spend per week for each household
    df_avg_spend = df_hh_week.groupby('HSHD_NUM')['SPEND'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    df_avg_spend.plot(ax=ax, kind='line', x='HSHD_NUM', y='SPEND')
    ax.set_xlabel('Household Number')
    ax.set_ylabel('Average Spend per Week')
    ax.set_title('Trend of Average Spend per Week per Household')
    return encode(fig)

# CHRISTMAS SEASON INSIGHT!
def total_spend_per_week(temp):
    df = temp.copy()
    # group by week and household, summing up the spend
    df_hh_week = df.groupby([pd.Grouper(key='WEEK_NUM'), pd.Grouper(key='HSHD_NUM')])['SPEND'].sum().reset_index()

    # group by week and calculate the average spend per household per week
    df_avg_week = df_hh_week.groupby('WEEK_NUM')['SPEND'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(df_avg_week['WEEK_NUM'], df_avg_week['SPEND'])
    ax.set_xlabel('Week Number')
    ax.set_ylabel('Average Spend per Household per Week')
    ax.set_title('Average Spend per Household per Week over Time')
    return encode(fig)

# QUESTION 2 - A
def hh_size_engagement(temp):
    df = temp.copy()
    # calculate average number of transactions per week for each household size
    df_size_engage = df.groupby(['HH_SIZE'])['BASKET_NUM'].nunique() / df['WEEK_NUM'].nunique()
    fig, ax = plt.subplots(figsize=(8, 6))
    df_size_engage.plot(kind='bar', ax=ax)
    ax.set_xlabel('Household Size')
    ax.set_ylabel('Average Number of Transactions per Week')
    ax.set_title('Relationship between Household Size and Customer Engagement')
    return encode(fig)

def children_engagement(temp):
    df = temp.copy()
    # calculate average number of transactions per week for each household's children count
    df_size_engage = df.groupby(['CHILDREN'])['BASKET_NUM'].nunique() / df['WEEK_NUM'].nunique()
    fig, ax = plt.subplots(figsize=(8, 6))
    df_size_engage.plot(kind='bar', ax=ax)
    ax.set_xlabel('Number of Children')
    ax.set_ylabel('Average Number of Transactions per Week')
    ax.set_title('Relationship between Number of Children and Customer Engagement')
    return encode(fig)

def income_engagement(temp):
    df = temp.copy()
    # calculate average number of transactions per week for each household size
    df_size_engage = df.groupby(['INCOME_RANGE'])['BASKET_NUM'].nunique() / df['WEEK_NUM'].nunique()
    fig, ax = plt.subplots(figsize=(8, 6))
    df_size_engage.plot(kind='bar', ax=ax)
    ax.set_xlabel('Income Range')
    ax.set_ylabel('Average Number of Transactions per Week')
    ax.set_title('Relationship between Income Range and Customer Engagement')
    return encode(fig)

# QUESTION 2 - B


def hhsize_department(temp):
    df = temp.copy()
    # group by household size and category, summing up the spend
    df_hh_size_cat = df.groupby(['HH_SIZE', 'DEPARTMENT'])['SPEND'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(12, 8))
    for key, grp in df_hh_size_cat.groupby(['HH_SIZE']):
        ax = grp.plot(ax=ax, kind='line', x='DEPARTMENT', y='SPEND', label=key)
    ax.set_xlabel('Commodity')
    ax.set_ylabel('Total Spend')
    ax.set_title('Total Spend per Household Size and Department')
    return encode(fig)

def children_department(temp):
    df = temp.copy()
    # group by household size and category, summing up the spend
    df_children_cat = df.groupby(['CHILDREN', 'DEPARTMENT'])['SPEND'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(12, 8))
    for key, grp in df_children_cat.groupby(['CHILDREN']):
        ax = grp.plot(ax=ax, kind='line', x='DEPARTMENT', y='SPEND', label=key)
    ax.set_xlabel('Commodity')
    ax.set_ylabel('Total Spend')
    ax.set_title('Total Spend per Children count and Department')
    return encode(fig)

def income_department(temp):
    df = temp.copy()
    # group by household size and category, summing up the spend
    df_income_cat = df.groupby(['INCOME_RANGE', 'DEPARTMENT'])['SPEND'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(12, 8))
    for key, grp in df_income_cat.groupby(['INCOME_RANGE']):
        ax = grp.plot(ax=ax, kind='line', x='DEPARTMENT', y='SPEND', label=key)
    ax.set_xlabel('Commodity')
    ax.set_ylabel('Total Spend')
    ax.set_title('Total Spend per Income Range and Department')
    return encode(fig)