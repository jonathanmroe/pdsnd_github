import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }




def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        answer = input('What city are you wanting to see the schedule for? ')
        if answer.lower() in CITY_DATA:
            city = CITY_DATA.get(answer.lower())
            print("OK. You're wanting the schedule for " + answer.title() +'.')
            break
        else:
            print("Sorry, didn't recognize your answer, try again")
    # get user input for month (all, january, february, march, april, may, june)
    months = ['all','january','february','march','april','may','june']
    while True:
        month = input('For what month? ')
        if month.lower() in months:
            print('O.K., for %s.' % month)
            break
        else:
            print('Sorry I don\'t have information for that month. Enter a month or enter \'all\'.')

    # get user input for day of week (all, monday, tuesday, wednesday, etc.)
    days = ['all','sunday','monday','tuesday','wednesday','thursday','friday','saturday']
    while True:
        day = input('For what day of the week? ')
        if day.lower() in days:
            print('O.K. for %s.' % day)
            break
        else:
            print('Sorry I don\'t think that is an actual day. Enter a day or enter \'all\'.')

    print('-'*40)
    return city, month, day

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
    city = str(city)
    df = pd.read_csv(city)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    # We created month and day of week columns (for version control project)
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    LIMIT = 10
    START = 0
    END = 10
    print('Here are the first 10 records for the city, month, and day you selected:') 
    print(df[START:END])
    while True:
        someMore = input('Do you want the next 10 records? yes or no: ')
        print(someMore)
        if someMore == 'yes':
            START = START + LIMIT
            END = END + LIMIT
            print(df[START:END])
        else:
            print('O.K. Moving on.')
            break
    print('-'*40)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    df['hour'] = df['Start Time'].dt.hour

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
     
    # display the most common month
    #print(df.month.mode())
    print('\nMost popular start month is %s.' % df['month'].apply(lambda x: calendar.month_name[x]).mode().values[0])

    # display the most common day of week
    print('\nMost popular start day is %s.' % df.day_of_week.mode().values[0])


    # display the most common start hour
    print("\nMost popular start hour is %s." % df.hour.mode().values[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('\nThe most popular start station is %s.' % df['Start Station'].mode().values[0])

    # display most commonly used end station
    print('\nThe most popular end station is %s.' % df['End Station'].mode().values[0])


    # display most frequent combination of start station and end station trip
    startStop = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False)
    print('\nPopular start and end: ' + str(startStop.index[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    Total = df['Trip Duration'].sum()
    print('Total travel time is %s' % Total)

    # display mean travel time
    averageTime = df['Trip Duration'].mean()
    print('\nAverage travel time is %s.' % averageTime)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    idx = pd.Index(df, name = 'User Type')
    user_types = df['User Type'].value_counts()
    print(user_types.to_string())
    print('-'*15)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print(gender.to_string())
    else:
        print('No gender information found.')
    print('-'*15)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        idx = pd.Index(df, name = 'Birth Year')
        birthYear = df['Birth Year'].value_counts()
        print('The earliest birth year is %d.' %int(birthYear.index.min()))
        print('\nThe most recent birth year is %d.' %int(birthYear.index.max()))
        commonYear = df['Birth Year'].mode().values[0]
        print('\nThe most common birth year is %d.' % int(commonYear))
    else:
        print('\nNo birth year information found.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

