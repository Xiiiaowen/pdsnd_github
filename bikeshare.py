"""
Exploring US Bike Share Data
Project Overview 
This project analyzes bike share system data from three major US cities: Chicago, New York City, and Washington, DC. 
Using data provided by Motivate, we will uncover usage patterns and compare system behavior across these cities.
"""

# 0. Import library and define some functions that could be reusable for later analysis
import numpy as np
import pandas as pd
import time
import os

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv',}

# 1. Define a function to get the filter conditions from user input (handling invalid inputs)
def get_filter():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore US bikeshare data together!')
    # get user input for city (chicago, new york city, washington)
    while True:
        city = input('\nPlease choose a city to analyze (chicago, new york city, washington): ').lower()
        if city in CITY_DATA.keys():
            break
        else:
            print('Invalid input. Please choose from: chicago, new york city, washington')

    # get user input for month (all, january, february, ..., june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input('\nPlease choose a month to analyze (all, january, february, ..., june): ').lower()
        if month in months:
            break
        else:
            print('Invalid input. Please choose from: all, january, february, march, april, may, june')

    # get user input for day of week (all, monday, tuesday, ..., sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input('\nPlease choose the weekday to analyze (all, monday, tuesday, ..., sunday): ').lower()
        if day in days:
            break
        else:
            print('Invalid input. Please choose from: all, monday, tuesday, wednesday, thursday, friday, saturday, sunday')

    
    print('-'*40)
    return city, month, day


# 2. Define a function to load and filter the data according to user demand
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load a data file into dataframe
    file_path = os.path.join(os.path.dirname(__file__), CITY_DATA[city])
    df = pd.read_csv(file_path)

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()  #when using day_name(), must add()

    # Filter by month if applicable (i.e. month input is not 'all')
    if month != 'all':
        # month input is word rather than number (df['month'] column), need to create a connection
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        # filter by month
        df = df[df['month'] == month]

    # Filter by day of week if applicable (i.e. day input is not 'all')
    if day != 'all':
        # day input from last function is in lower case, capitalize the first letter to be
        # compatible with df['day_of_week'] column
        df = df[df['day_of_week'] == day.title()]
 
    return df


# 3. Define a function to analyze the Popular Times of Travel for question #1
def time_stats(df):
     """Displays statistics on the most frequent times of travel."""

     print('\nCalculating The Most Frequent Times of Travel...\n')
     start_time = time.time()

     # display the most common month
     months = ['january', 'february', 'march', 'april', 'may', 'june']
     most_common_month = months[df['month'].mode()[0] - 1].title()
     print('Most Popular month of travel is: {}.'.format(most_common_month))

     # display the most common day of week
     print('Most Popular weekday of travel is: {}'.format(df['day_of_week'].mode()[0]))

     # display the most common start hour
     most_common_hour = df['Start Time'].dt.hour.mode().iloc[0]  # use iloc[] to avoid ambiguiouty
     print('Most Popular start hour of travel is: {}'.format(most_common_hour))

     print('\nThis took %s seconds.' % (time.time() - start_time))
     print('-'*40)


# 4. Define a function to analyze the Popular Stations and trip for question #2
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popualar Stations and Trip...\n')
    start_time = time.time()

    # display a most commonly used start station
    print('\nThe most commonly used start station is: {}.'.format(df['Start Station'].mode()[0]))

    # display a most commonly used end station
    print('\nThe most commonly used start station is: {}.'.format(df['End Station'].mode()[0]))

    # display a most commonly used start station
    df['Start-End'] = df['Start Station'] + ' - ' + df['End Station']
    print('\nMost frequent combination of start station and end station trip is: {}.'.format(
        df['Start-End'].mode()[0]))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)
    

# 5. Define a function to analyze Trip Duration for question #3
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # calculate the total and average travel time in seconds
    total_travel_seconds = df['Trip Duration'].sum()
    average_travel_seconds = df['Trip Duration'].mean()

    # convert to more readable formats - total (days, hours, minutes), average (minutes, seconds)
    total_days = total_travel_seconds // (24 * 3600)
    total_hours = (total_travel_seconds % (24 * 3600)) // 3600
    total_minutes = (total_travel_seconds % 3600) // 60
    total_seconds = total_travel_seconds % 60

    average_minutes = average_travel_seconds // 60
    average_seconds = average_travel_seconds % 60

    # display total travel time - converted seconds to meaningful units (days, hours, minutes)
    print('Total travel time: ')
    if total_days > 0:
        print(f'{total_days:.0f} days, {total_hours:.0f} hours, {total_minutes:.0f} minutes, {total_seconds:.0f} seconds.')
    elif total_hours > 0:
        print(f'{total_hours:.0f} hours, {total_minutes:.0f} minutes, {total_seconds:.0f} seconds.')
    else:
        print(f'{total_minutes:.0f} minutes, {total_seconds:.0f} seconds.')

    print(f'({total_travel_seconds:,.0f} seconds total)')

    # display average travel time - converted seconds to meaningful units (minutes, seconds)
    print('Average travel time: ')
    if average_minutes > 0:
        print(f'{average_minutes:.0f} minutes, {average_seconds:.0f} seconds.')
    else:
        print(f'{average_seconds:.0f} seconds.')

    print(f'({average_travel_seconds:,.0f} seconds total)')


    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


# 6. Define a function to analyze User Information for question #4
def user_stats(df):
    """Displays statistics on bikeshare users."""
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Type Distribution:')
    for user_type, count in user_types.items():
        print(f'{user_type}: {count:,}')
    print()

    # Display counts of gender - washington has no Gender variable
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('Gender Counts Distribution:')
        for gender, count in gender_counts.items():
            print(f'{gender}: {count:,}')
        print()
    else:
        print('Gender Data is not available for this city.\n')


    # Display counts of Birth Year - washington has no Gender variable
    shortest = df['Trip Duration'].min()
    longest = df['Trip Duration'].max()
    average = df['Trip Duration'].mean()

    shortest_minutes = shortest // 60
    shortest_seconds = shortest % 60

    longest_minutes = longest // 60
    longest_seconds = longest % 60

    average_minutes = average // 60
    average_seconds = average % 60

    # display subscriber shortest travel time
    print('Shortest travel time: ')
    if shortest_minutes > 0:
        print(f'{shortest_minutes:.0f} minutes, {shortest_seconds:.0f} seconds.')
    else:
        print(f'{shortest_seconds:.0f} seconds.')
    print(f'({shortest:,.0f} seconds total)')

    # display subscriber longest travel time
    print('Longest travel time: ')
    if longest_minutes > 0:
        print(f'{longest_minutes:.0f} minutes, {longest_seconds:.0f} seconds.')
    else:
        print(f'{longest_seconds:.0f} seconds.')
    print(f'({longest:,.0f} seconds total)')
        
    # display subscriber average travel time
    print('Average travel time: ')
    if average_minutes > 0:
        print(f'{average_minutes:.0f} minutes, {average_seconds:.0f} seconds.')
    else:
        print(f'{average_seconds:.0f} seconds.')
    print(f'({average:,.0f} seconds total)')

   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# 7. Define a function to analyze User Information for question #5
def subscriber_stats(df):
    """Displays statistics on bikeshare subscribers."""
    
    print('\nCalculating Subscriber Stats...\n')
    start_time = time.time()

    # Filter out Subscriber data and create a copy to avoid SettingWithCopyWarning
    subscriber_df = df[df['User Type'] == "Subscriber"].copy()

    # Display counts of gender - washington has no Gender variable
    if 'Gender' in subscriber_df.columns:
        sub_gender_counts = subscriber_df['Gender'].value_counts()
        print('Subscriber Gender Counts Distribution:')
        for gender, count in sub_gender_counts.items():
            print(f'{gender}: {count:,}')
        print()
    else:
        print('Gender Data is not available for this city.\n')


    # Display counts by birth year groups - washington has no Gender variable
    # (<1980, 1980-1989, 1990-1999, 2000-2009, >2010)
    if 'Birth Year' in subscriber_df.columns:
        bins = [0, 1980, 1990, 2000, 2010, 3000]
        labels = ['<1980', '1980-1989', '1990-1999', '2000-2009', '>2010']
        # Create 'Birth_Year_Group'
        subscriber_df['Birth_Year_Group'] = pd.cut(subscriber_df['Birth Year'], bins=bins, labels=labels, right=False)
        
        # Sort by the chronological order of the bins, not by count frequency
        birth_year_group_counts = subscriber_df['Birth_Year_Group'].value_counts()
        
        # Reindex to force the correct chronological order
        birth_year_group_counts = birth_year_group_counts.reindex(labels)

        print('Subscriber Birth Year Group Counts Distribution:')
        for year_group, count in birth_year_group_counts.items():
            print(f'{year_group}: {count:,}')
        print()
    else:
        print('Birth Year Data is not available for this city.\n')


    if 'Birth Year' in df.columns:        
        earliest = int(subscriber_df['Birth Year'].min())
        recent = int(subscriber_df['Birth Year'].max())
        common = int(subscriber_df['Birth Year'].mode()[0])
        print('Birth Year Statistics:')
        print(f'Earliest: {earliest}')
        print(f'Most recent: {recent}')
        print(f'Most common: {common}')
    else:
        print('Birth Year Data is not available for this city.\n')

   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# 8. Define a function to display raw data upon request
def display_raw_data(df):
    """Displays raw data in chunks of 5 rows upon user request."""
    start_index = 0
    while True:
        show_raw = input("\nWould you like to see 5 lines of raw data? Enter yes or no: ").lower()
        if show_raw == 'no':
            print('\nNo more raw data to display.')
            break
        elif show_raw == 'yes':
            # Check if there is more data to display
            if start_index < len(df):
                print(f'\nDisplaying rows {start_index + 1} to {min(start_index + 5, len(df))}: ')
                print(df.iloc[start_index:start_index+5])
                start_index += 5
            else:
                print("\nNo more raw data to display")
                break
        else:
            print('Invalid input. Please enter yes or no.')



# 9. Use the functions and define a main function to interact with User for Analysis
def main():
    while True:
        city, month, day = get_filter()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        subscriber_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()










