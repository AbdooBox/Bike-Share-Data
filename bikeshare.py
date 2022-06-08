import time
import pandas as pd
import numpy as np
import calendar


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'septemper', 'october', 'november', 'december','all' ]
#months = [0] + 1
DAYS = [calendar.day_name[i].lower() for i in range(7)]  + ["all"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input("Which city you would like to explore: ").lower()
    if city not in CITY_DATA:
        # city user entered is not a valid city
        print(f"The city you entered ({city}) is not currently supported.")
        print(f"Please enter a valid city [{', '.join(CITY_DATA.keys())}]")
        exit()

    # TO DO: get user input for month (all, january, february, ... , june)

    month = input("Which month you would like to explore: ").lower()
    #[calendar.month_name[i].lower() for i in range(1, 13)]
    trials = 0
    while month not in MONTHS:
        trials += 1
        if trials > 3:
            print("Three failed trials, exiting!")
            exit()
        print('kindly give a valid month name:')
        month = input("Which month you would like to explore: ").lower()
        
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    day = input("Choose a day of week name you would like to explore: ").lower()
    trials = 0
    while day not in DAYS:
        trials += 1
        if trials > 3:
            print("Three failed trials, exiting!")
            exit()
        print('you still have a chance to enter a valid input otherwise the program will terminate!')
        day = input("Choose a day of week name you would like to explore: ").lower()

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
    df = pd.read_csv(CITY_DATA[city])
    # print(df.head())
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month # month index
    month = MONTHS.index(month) + 1

    #print(df["month_index"])

    # df['month'] = df["month_index"].apply(lambda x: MONTHS[x - 1])

    # print(df["month"])
    #df['month'] = df["month_index"].apply(lambda x: calendar.month_name[x].lower())
    #df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()


    if month != "all":
        df = df[df.month == month]
    if day != "all":
        df = df[df.day_of_week == day]
    
    # print(df.head())

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    print(df['month'].mode())

    # TO DO: display the most common day of week
    
    #if specified all days not a single one.
    
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    popular_day = df['day_of_week'].mode()[0]
    print('the most comon day of the week:', popular_day)
    
    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most comon start hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most commonly used Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    
    start_station = df['Start Station'].mode()[0]
    print('most commonly used start station:', start_station)
    
    # TO DO: display most commonly used end station
    
    end_station = df['End Station'].mode()[0]
    print('most commonly used end station:', end_station)

    # TO DO: display most frequent combination of start station and end station trip

    most_frequent_combination = (df['Start Station'] + " & " + df['End Station']).mode()[0]
    print('most frequent combination of start station and end station trip:', most_frequent_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time

    total_travel_time = df['Trip Duration'].sum()
    print('total travel time:', int(total_travel_time))

    # TO DO: display mean travel time

    mean_travel_time = df['Trip Duration'].mean()
    print('average travel time:', int(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types

    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender

    try:

        print(df['Gender'].value_counts())
    except:
        print('data is not available at the moment')

    # TO DO: Display earliest, most recent, and most common year of birth
    
    try:
        earliest_date = df['Birth Year'].min()
        most_recent_date = df['Birth Year'].max()
        most_common_date = df['Birth Year'].mode()[0]
        print('Earliest date of birth: ',int(earliest_date))
        print('\nMost recent date of birth: ',int(most_recent_date))
        print('\nMost common date of birth: ',int(most_common_date))
    except:
        print('Birth Year isn\'t available in data provided.')


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
