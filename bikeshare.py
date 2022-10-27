import time
import pandas as pd

city_data = {'chicago': 'chicago.csv','new york city': 'new_york_city.csv','washington': 'washington.csv'}
month_data = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
day_data = ['all', 'monday', 'tuesday', 'wednesday','thursday', 'friday', 'saturday', 'sunday']

#Opening message waiting for user input
print('Hello! Let\'s explore some US bikeshare data!')
   
def invalid_input():
    '''user entered invalid input that did not match what the program was asking for.
    So is prompted to try again'''
    print('\n--- Invalid input. Please try again ---')

def horiz_separator():
    '''function used repeatedly to print horizontal lines for easy readability of output'''
    print('-'*40)

def filter_select():
    '''
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or 'all' to apply no month filter
        (str) day - name of the day of week to filter by, or 'all' to apply no day filter
        (str) month_filter_yn - if the user wants to apply a month filter
        (str) day_filter_yn - if the user wants to apply a day filter
    '''
    
    # get user input for city (chicago, new york city, washington)
    city = ''
    while city not in city_data:
        city = input('\nInput a city - Chicago, New York City, Washington.\n> ').lower()
        if city in city_data:
            break
        else:
            # tell user their input was invalid, as it did not meet the input requirements
            invalid_input()
    # get user input for month (all, january, february, ... , june)
    month_filter_yn = ''
    month = ''
    #ask if user wants to filter by month
    while month_filter_yn not in ('y','n'):
        month_filter_yn = input('\nWould you like to filter by month? (Y or N)\n> ').lower()
        # if yes then run month selection
        if month_filter_yn == 'y':
            print(month_filter_yn.title(),'selected.')
            #yes was inputted by the user, next promp user for month select
            break
        elif month_filter_yn == 'n':
            #no was inputted by the user, skip month select
            print(month_filter_yn.title(),'selected.')
            month = month_data[0]
            break
        else:
            invalid_input()
            continue
    
    # if user inputs yes, prompt month selection
    while month_filter_yn == 'y':
        month_name = input('\nInput a month to filter by - Between January and June\n> ').lower()
        if month_name.lower() in month_data:
        #month was inputted by the user from month_data
            print(month_name.title(),'selected.')
            month = month_name.lower()
            break
        else:
            invalid_input()
            continue

    #ask if user wants to filter by day
    day_filter_yn = ''
    day = ''
    while day_filter_yn not in ('y','n'):
        day_filter_yn = input('\nWould you like to filter by day? (Y or N)\n> ').lower()
        if day_filter_yn == 'y':
            print(day_filter_yn.title(),'selected.')
            #yes was inputted by the user, next promp user for day
            break
        elif day_filter_yn == 'n':
            #no was inputted by the user, skip day select
            print(day_filter_yn.title(),'selected.')
            day = day_data[0]
            break
        else:
            invalid_input()
            continue

    #prompts user for day to filter by. This is not run if user previously said no to day select
    while day not in day_data:   
        day = input('Input a day of the week to filter by: \n> ').lower()
        if day in day_data:
            break
        else:
            invalid_input()
    return city, month, day


def load_data(city, month, day):
    '''
    Loads data for the specified city and filters by month and day if applicable. 
    Using Pandas dataframe containing city data filtered by user
    '''
    print('\n\n---[ ACTIVE FILTERS ]---')
    print('Data displayed is using the following filters:\n') 
    print('City: ' + city.title())
    print('Month: ' + month.title()) 
    print('Day: ' + day.title()) 

     # load data file into a dataframe
    df = pd.read_csv(city_data[city])
    
    #convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month. Skip if user said no to month filter
    if month != 'all':
        # use the index of the months list to get the month num
        months = month_data
        month = months.index(month)
    
        # filter by month to create df
        df = df[df['month'] == month]

    # filter by day. Skip if user said N to day filter
    if day != 'all':
        # filter by day of week to create the new dataframe
        
        df = df[df['day_of_week'] == day.title()]

    horiz_separator()
    return df


def time_stats(df):
    '''statistics on the most frequent times of travel.'''
    print('\nCalculating The Most Frequent Times of Travel...')
    #returns a time estimate of how long the load took to run. Formatted to 3 decimal places
    start_time = time.time()
    print('This took %s seconds.' % '{:.3f}'.format((time.time() - start_time)),'\n')

    print('\n---[ TIMES OF TRAVEL ]---\n') 
    # display the most common month
    print('- Most common month:', df['month'].mode()[0])

    # display the most common day of week
    print('- Most common day of week:', df['day_of_week'].mode()[0])

    # display the most common start hour in 24 hr time
    df['hour'] = df['Start Time'].dt.hour
    print('- Most common start hour:', df['hour'].mode()[0],': 00')
    
    horiz_separator()


def station_stats(df):
    '''statistics on the most popular stations and trips'''
    print('\nCalculating The Most Popular Stations and Trips...')
    start_time = time.time()
    print('This took %s seconds.' % '{:.3f}'.format((time.time() - start_time)),'\n')

    print('\n---[ STATIONS AND TRIPS ]---\n') 
    # display most commonly used start station
    print('- Most common start station: ', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('- Most common end station: ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + ' ' + df['End Station']
    print('- Most common combination of start and end station: ', df['combination'].mode()[0])

    horiz_separator()


def trip_duration_stats(df):
    '''statistics on the total and trip duration'''
    print('\nCalculating Trip Duration...')
    start_time = time.time()
    print('This took %s seconds.' % '{:.3f}'.format((time.time() - start_time)),'\n')

    print('\n---[ TRIP DURATION ]---\n') 

    #convert seconds to hours and set to 3 decimal places
    total_travel_time = '{:.3f}'.format(df['Trip Duration'].sum()/3600)
    # total travel time
    print('- Total travel time:',total_travel_time,'hours.')

    #convert seconds to minutes and set to 3 decimal places
    avg_travel_time = '{:.3f}'.format(df['Trip Duration'].mean()/60)
    # average travel time
    print('- Average travel time:',avg_travel_time,'minutes.')

    horiz_separator()


def user_stats(df, city):
    '''statistics on bikeshare users'''
    print('\nCalculating User Stats...')
    start_time = time.time()
    print('This took %s seconds.' % '{:.3f}'.format((time.time() - start_time)),'\n')

    user_types = df['User Type'].value_counts()
    print('\n---[ USER TYPES ]---\n') 
    print('User Type:\n')
    print(user_types)
    if city in ('chicago','new york city'):
        # counts of gender (not available in washington data)
        gender = df['Gender'].value_counts()
        print('\nNumber of users by gender: \n')
        print(gender)
        # earliest, most recent, and most common year of birth
        min_birth_year = df['Birth Year'].min()
        max_birth_year = df['Birth Year'].max()
        mode_birth_year = df['Birth Year'].mode()[0]

        print('\nBirth year stats: \n')
        print('- Earliest birth year:','{:.0f}'.format(min_birth_year))
        print('- Most recent birth year:','{:.0f}'.format(max_birth_year))
        print('- Most common birth year:','{:.0f}'.format(mode_birth_year))

    horiz_separator()
    
def raw_data(df):
    '''#raw data section. asks user if they want to see raw data or not.
    if yes, they can continuously view 5 rows of consecutive data.
    if no, this section is skipped'''
    print('\n---[ RAW DATA ]---\n') 
    #print the number of rows filtered by
    print('There are',len(df),'total rows of data. (Filters are active) \n')
    start = 0
    raw_data_rows = 5
    raw_data_rows_left = len(df)-5
    #print message before seeing data
    msg = '\nWould you like to see 5 rows of raw data? (Y or N)\n> '
    view_raw_yn =''
    #if the number of rows left to view is 0, it will not show more data 
    while raw_data_rows < len(df)+5:
        view_raw_yn = input(msg).lower()
        if view_raw_yn == 'y':
            print('\n',raw_data_rows_left,'rows left of data to view. \n')
            print(df[start:raw_data_rows])
            #setup variables for counting how many rows have been viewed, and how many are left
            raw_data_rows = raw_data_rows + 5
            raw_data_rows_left = raw_data_rows_left - 5
            start = raw_data_rows - 5

            #change msg once already seen rows. Adds 'more'
            msg = '\nView 5 more rows? (Y or N)\n> '

        #if user doesnt want to view raw data, skip section
        elif view_raw_yn == ('n'):
            break
        else:
            invalid_input()
            continue      


def project():
    '''Main script to run through'''
    while True:
        city, month, day = filter_select()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)
        restart_yn()

def restart_yn():
    restart = ''
    '''function to determine if user wants to start from beginning or exit
    Runs at the end of the main project() function'''
    while restart not in ('y','n'):
        restart = input('\nWould you like to start from the beginning? Input Y or N: \n> ').lower()
        if restart == ('y'):
            print('\nPROGRAM RESTARTED! ')
            project()
        elif restart == ('n'):
            print('\nPROGRAM ENDED. ')
            exit()
        else:
            invalid_input()
            continue

#main function            
project()

