import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Clean data
df = df[(df.value >= df.value.quantile(0.025)) & (df.value <= df.value.quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig, axes = plt.subplots(figsize=(20, 12))
    
    axes.plot(df, color='red')
    axes.set_xlabel('Date')
    axes.set_ylabel('Page Views')
    axes.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    fig

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['Years'] = df_bar.index.year
    df_bar['Month'] = df_bar.index.month_name()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_bar['Month'] = pd.Categorical(df_bar['Month'], categories=month_order, ordered=True)
    df_bar = df_bar.sort_values(by=['Years', 'Month'])

    # Draw bar plot
    g = df_bar.groupby(['Years', 'Month'])['value'].sum().unstack().plot(ylabel='Average Page Views',kind='bar', figsize=(12, 16))
    
    fig = g.figure


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['Years'] = [d.year for d in df_box.date]
    df_box['Month'] = [d.strftime('%b') for d in df_box.date]
    
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['Month'] = pd.Categorical(df_box['Month'], categories=month_order, ordered=True)
    df_box = df_box.sort_values(by=['Years', 'Month'])

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(nrows=1, ncols= 2, figsize=(20,16))
    sns.boxplot(data=df_box, x='Years', y='value', hue='Years', palette='Set3', ax=ax[0])
    ax[0].set_title('Year-wise Box Plot (Trend)')
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Page Views')
    ax[0].set_yticklabels(['0', '20000', '40000', '60000', '80000', '100000', '120000', '140000', '160000', '180000', '200000'])
    sns.boxplot(data=df_box, x='Month', y='value', hue='Month', palette='Set3', ax=ax[1])
    ax[1].set_title('Month-wise Box Plot (Seasonality)')
    ax[1].set_xlabel('Month')
    ax[1].set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
