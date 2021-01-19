import datetime
import time
import pandas as pd
import numpy as np
import sys

def get_filters():
    #initialize and clear variables used
    #City files are controlled by this dictionary
    CITY_DATA = { 'chicago': 'chicago.csv', 'new york': 'new_york_city.csv', 'washington': 'washington.csv' }

    #filters are controlled through these options based on what is in the data
    filter_list = ['month', 'day', 'both', 'none']
    months_list = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    days_list = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

    city = ''
    sel_filter = ''
    focus_month = ''
    focus_day = ''

    #Get city for analysis focus
    city = input('Would you like to look at Chicago, New York or Washington?')
    file_name = CITY_DATA.get(city.lower())
    while len(city)<=2 and file_name is None:
        city = str(input("Try again, only select the cities on the list:"))

    print("It looks like you are interested in data for",city.title(),".  If this is not correct please restart the program.")

    #Get filter approach for looking at data
    sel_filter = str(input('Would you like to filter the data by month, day, both, or not at all?  Type  "none" for no time filter.'))

    while sel_filter.lower() not in filter_list:
        sel_filter = str(input("Try again, only select the filter options on the list:"))

    if sel_filter.lower() == 'month':
        print("Filtering by month")
        focus_month = str(input('Which month?  January, February, March, April, May, June or all?'))
        focus_day = 'all'
        while focus_month.lower() not in months_list:
            focus_month = str(input("Try again, only select the filter options on the list:"))

    elif sel_filter.lower() == 'day':
        print("Filtering by day of the week")
        focus_day = str(input('Which day?  Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or all?'))
        focus_month = 'all'
        while focus_day.lower() not in days_list:
            focus_day = str(input("Try again, only select the month options on the list:"))

    elif sel_filter.lower() == 'both':
        print("Filtering by month and day of the week")
        focus_month = str(input('Which month?  January, February, March, April, May, June or all?'))
        while focus_month.lower() not in months_list:
            focus_month = str(input("Try again, only select the month options on the list:"))

        focus_day = str(input('Which day?  Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or all?'))
        while focus_day.lower() not in days_list:
            focus_day = str(input("Try again, only select the month options on the list:"))

    else:
        print("No filters will be applied")
        sel_filter = 'none'
        focus_day = 'all'
        focus_month = 'all'

    print ('Selected filters are ', city, sel_filter, focus_month, focus_day)

    print('-'*40)

    return(city, focus_month, focus_day)

def load_data(city, focus_month, focus_day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    CITY_DATA = { 'chicago': 'chicago.csv', 'new york': 'new_york_city.csv', 'washington': 'washington.csv' }
    filter_list = ['month', 'day', 'both', 'none']
    months_list = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    days_list = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

    fullpath = './'+ CITY_DATA[city.lower()]

    df = pd.read_csv(fullpath)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if focus_month.lower() != 'all':
        # use the index of the months list to get the corresponding int
        focus_month = months_list.index(focus_month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == focus_month]

    # filter by day of week if applicable
    if focus_day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == focus_day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month from the Start Time column to create an month column
    df['month'] = df['Start Time'].dt.month
    # find the most popular hour
    common_month = df['month'].mode()[0]

    print('Most Common Month:', common_month)

    # display the most common day of week
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract day from the Start Time column to create an day column
    df['day'] = df['Start Time'].dt.day
    # find the most popular day
    common_day = df['day'].mode()[0]

    print('Most Common Day:', common_day)

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    input("Press Enter to continue...")

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]

    print('Most Common Start station:', common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]

    print('Most Common End station:', common_end)

    # display most frequent combination of start station and end station trip
    x = str(df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).head(1).index[0])
    x = x.replace('(', '').replace(')', '').replace("'", '')
    print('Most frequent combination of start and end station: ',x.strip())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    input("Press Enter to continue...")

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Display total travel time
    print('Total Travel Time: ', seconds_to_datestamp(df['Trip Duration'].sum()))
    #print('Total Travel Time: ', df['Trip Duration'].sum())

    #Display mean travel time
    print('Mean Travel Time: ', seconds_to_datestamp(df['Trip Duration'].mean()))
    #print('Mean Travel Time: ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    input("Press Enter to continue...")

def seconds_to_datestamp(input_seconds):
    #Code snippet obtained from https://www.w3resource.com/python-exercises/python-basic-exercise-65.php and modified to suit#
    day = input_seconds // (24 * 3600)
    input_seconds = input_seconds % (24 * 3600)
    hour = input_seconds // 3600
    input_seconds %= 3600
    minutes = input_seconds // 60
    input_seconds %= 60
    seconds = input_seconds
    return'{0:.0f} days, {1:.0f} hours, {2:.0f} minutes, {3:0f} seconds'.format(day, hour, minutes, seconds)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    if 'User Type' in df.columns:
        x = '\n' + df['User Type'].value_counts().to_string()
    else:
        x = 'N/A'
    print('Count of user types: {}'.format(x))

    #Display counts of gender
    if 'Gender' in df.columns:
        x = '\n' + df['Gender'].value_counts().to_string()
    else:
        x = 'N/A'
    print('\nCount of Genders: {}'.format(x))

    #Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        x = int(df['Birth Year'].min())
    else:
        x = 'N/A'
    print('\nEarliest year of birth: {}'.format(x))

    if 'Birth Year' in df.columns:
        x = int(df['Birth Year'].max())
    else:
        x = 'N/A'
    print('\n Most recent birth year: {}'.format(x))

    if 'Birth Year' in df.columns:
        x = int(df['Birth Year'].mode()[0])
    else:
        x = 'N/A'
    print('Most common year of birth: {}'.format(x))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    input("Press Enter to continue...")

def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    view_display= ''
    start_loc = 0
    while (view_display !='no'):
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_display = input("Do you wish to continue?: ").lower()

def main():
    while True:
        print("Welcome let's have a look at some US Bikeshare data analysis\n")
        print("You will be asked to press enter to move between the various analysis sections\n\n")
        print('-'*40)

        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        print ("The dataframe for analysis contains:", len(df), "rows of data.")
        print ("The dataframe analysed contained NaN values in these columns:\n",df[df.columns[df.isna().any()]]," NaN values.")
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
