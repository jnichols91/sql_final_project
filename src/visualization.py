import getpass
import pg8000
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import pandas as pd
import numpy as np

from datetime import datetime

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


plt.style.use('ggplot')

def get_fires(cursor, state_name):
    query = f"""SELECT DATE_PART('doy', disc_date) as day_of_year, avg(fire_size)
                FROM fires
                WHERE state=%s
                GROUP BY day_of_year
                ORDER BY day_of_year"""
    try:
        cursor.execute(query, (state_name, ))
        table = [row for row in cursor.fetchall()]
        columns = [col[0] for col in cursor.description]
        df = pd.DataFrame(table, columns=columns)
        # results = df.describe(include='all').iloc[0:2, :]
        # results.loc['na_count'] =  df.isna().sum()
    except pg8000.Error as e:
        messagebox.showerror('Database error', e)

    df['day_of_year'] = pd.to_datetime(df['day_of_year'], format='%j').dt.strftime('%b-%d')

    return df

def plot_fires(cursor):
    fl_fires = get_fires(cursor, 'FL')
    co_fires = get_fires(cursor, 'CO')

    days = mdates.DayLocator()
    months = mdates.MonthLocator()
    month_fmt = mdates.DateFormatter('%b-%d')

    fig1 = plt.figure(figsize=(8,6))
    ax1 = fig1.add_axes([0.1,0.15,0.9,0.75])
    ax1.plot(fl_fires['day_of_year'], fl_fires['avg'], label='Florida', color='red')
    ax1.plot(co_fires['day_of_year'], co_fires['avg'], label='Colorado', color='blue')
    ax1.set_xlabel('Day of Year')
    ax1.set_ylabel('Average Fire Size')
    ax1.set_title('Average Fire Size by Day of Year')
    ax1.legend(loc=0)
    ax1.xaxis.set_major_locator(months)
    ax1.xaxis.set_major_formatter(month_fmt)
    ax1.xaxis.set_minor_locator(days)
    ax1.format_xdata = mdates.DateFormatter('%b-%d')
    ax1.set_frame_on(True)

    fig1.autofmt_xdate()
    fig1.savefig('../figures/fires.png')
    plt.show()

def get_fires_class(cursor, state_name):
    query = f"""SELECT fire_size_class, count(*)
                FROM fires
                WHERE state=%s
                GROUP BY fire_size_class
                ORDER BY fire_size_class"""
    try:
        cursor.execute(query, (state_name, ))
        table = [row for row in cursor.fetchall()]
        columns = [col[0] for col in cursor.description]
        df = pd.DataFrame(table, columns=columns)
        # results = df.describe(include='all').iloc[0:2, :]
        # results.loc['na_count'] =  df.isna().sum()
    except pg8000.Error as e:
        messagebox.showerror('Database error', e)

    return df

def plot_fires_class(cursor):
    fl_fires_class = get_fires_class(cursor, 'FL')
    co_fires_class = get_fires_class(cursor, 'CO')

    fig2 = plt.figure(figsize=(8,6))
    ax2 = fig2.add_axes([0.1,0.1,0.9,0.8])
    ax2.bar(fl_fires_class['fire_size_class'], fl_fires_class['count'], label='Florida', color='red')
    ax2.bar(co_fires_class['fire_size_class'], co_fires_class['count'], label='Colorado', color='blue')
    ax2.set_xlabel('Class of Fire')
    ax2.set_ylabel('Number of Fires')
    ax2.set_title('Fires by Class')
    ax2.legend(loc=0)

    fig2.savefig('../figures/fires_class.png')
    plt.show()

def get_fires_regions(cursor, state_name):
    query = f"""SELECT DATE_PART('doy', disc_date) as day_of_year, avg(fire_size), eco_region
                FROM fires as f, regions as r
                WHERE f.state=%s
                AND f.fpa_id = r.fpa_id
                GROUP BY day_of_year, eco_region
                ORDER BY day_of_year"""
    try:
        cursor.execute(query, (state_name, ))
        table = [row for row in cursor.fetchall()]
        columns = [col[0] for col in cursor.description]
        df = pd.DataFrame(table, columns=columns)
        # results = df.describe(include='all').iloc[0:2, :]
        # results.loc['na_count'] =  df.isna().sum()
    except pg8000.Error as e:
        messagebox.showerror('Database error', e)

    df['day_of_year'] = pd.to_datetime(df['day_of_year'], format='%j').dt.strftime('%b-%d')

    return df

def plot_fires_regions(cursor):
    fl_fires_regions = get_fires_regions(cursor, 'FL')
    co_fires_regions = get_fires_regions(cursor, 'CO')

    days = mdates.DayLocator()
    months = mdates.MonthLocator()
    month_fmt = mdates.DateFormatter('%b-%d')

    fig3, ax3 = plt.subplots(figsize=(8, 6), nrows=1, ncols=2, dpi=100)

    ax3[0].set_title('Average Fire Size by Region (Florida)', fontsize=12)
    ax3[0].set_xlabel('Day of Year', fontsize=10)
    ax3[0].set_ylabel('Average Fire Size', fontsize=10)
    for region in fl_fires_regions['eco_region'].unique():
        ax3[0].plot(fl_fires_regions.loc[fl_fires_regions['eco_region']==region, 'day_of_year'],
                    fl_fires_regions.loc[fl_fires_regions['eco_region']==region, 'avg'], label=region)

    ax3[0].legend(loc=0, prop={'size': 5})
    ax3[0].xaxis.set_major_locator(months)
    ax3[0].xaxis.set_major_formatter(month_fmt)
    ax3[0].xaxis.set_minor_locator(days)
    ax3[0].format_xdata = mdates.DateFormatter('%b-%d')
    ax3[0].tick_params(labelsize=8)
    ax3[0].set_frame_on(True)

    ax3[1].set_title('Average Fire Size by Region (Colorado)', fontsize=12)
    ax3[1].set_xlabel('Day of Year', fontsize=10)
    ax3[1].set_ylabel('Average Fire Size', fontsize=10)

    for region in co_fires_regions['eco_region'].unique():
        ax3[1].plot(co_fires_regions.loc[co_fires_regions['eco_region']==region, 'day_of_year'],
                    co_fires_regions.loc[co_fires_regions['eco_region']==region, 'avg'], label=region)

    ax3[1].legend(loc=0, prop={'size': 5})
    ax3[1].xaxis.set_major_locator(months)
    ax3[1].xaxis.set_major_formatter(month_fmt)
    ax3[1].xaxis.set_minor_locator(days)
    ax3[1].format_xdata = mdates.DateFormatter('%b-%d')
    ax3[1].tick_params(labelsize=8)
    fig3.autofmt_xdate()
    ax3[1].set_frame_on(True)

    plt.tight_layout()

    fig3.savefig('../figures/fires_regions.png')
    plt.show()

    print(fl_fires_regions.head())


def main():
    user = 'jnichols2'
    secret = 'Nichols1'
    db = pg8000.connect(user=user, password=secret, host='bartik.mines.edu', database='csci403')
    cursor = db.cursor()

    plot_fires_regions(cursor)



if __name__ == '__main__':
    main()
