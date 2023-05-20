import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
month_list=['january', 'february', 'march', 'april', 'may', 'june','all']
weekday_list=['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']

#validate user input
def check_user_input(user_input,input_type):
    while True:
            input_user_entered=input(user_input).lower()
            try:
                if input_user_entered in ['chicago','new york city','washington'] and input_type == 'c':
                    break
                elif input_user_entered in month_list and input_type == 'm':
                    break
                elif input_user_entered in weekday_list and input_type == 'd':
                    break
                else:
                    if input_type == 'c':
                        print("Invalid input!")
                    if input_type == 'm':
                        print("Invalid input!")
                    if input_type == 'd':
                        print("Invalid input!")
            except ValueError:
                print("Your input is invalid. Please try again!")
    return input_user_entered

def get_filters(): 
    """
    Ask user to specify a city, month and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city and check validity
    city = check_user_input("Pleaese enter a city from (chicago, new york city or washington).\n",'c')
    # get user input for month and check validity  
    month = check_user_input("Please enter a month from (january, february, march, april, may, june). Type 'all' if no month filter.\n", 'm')
    # get user input for day of week and check validity
    day = check_user_input("Please enter a weekday from (monday, tuesday, wednesday, thursday, friday, saturday, sunday). Type 'all' if no weekday filter.\n", 'd')
    print('\nYour choice was :\ncity: {}\nmonth: {}\nday: {}\n'.format(city,month,day)) 
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
   # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and Hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    most_common_month = df['month'].mode()[0]
    print('Most Common Month is: ', most_common_month)

    #display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('Most Common Day Of Week is: ', most_common_day)

    #display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour Of Day is: ', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    most_commo_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station is: ', most_commo_start_station)

    #display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('Most Common End Station is: ', most_common_end_station)

    #display most frequent combination of start station and end station trip
    combination_group=df.groupby(['Start Station','End Station'])
    most_frequent_combination_station = combination_group.size().sort_values(ascending=False).head(1)
    print('Most frequent combination of Start Station and End Station trip is: ', most_frequent_combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time is: ', total_travel_time)


    #display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Average Travel Time is: ', mean_travel_time)

    #display largest and smallest duration of travel time
    print('Largest travel duration is: ',df['Trip Duration'].max())
    print('Smallest travel duration is: ',df['Trip Duration'].min())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #display counts of user types
    print('Counts of user types are: ',df['User Type'].value_counts())
  
    #display counts of gender
    #exclude Washington city
    if city != 'washington':
        #display counts of gender
        print('Counts Of Gender: ',df['Gender'].value_counts())
    else: print('Sorry, Wasington has no "Gender" information.')

    #display earliest, most recent, and most common year of birth
    #exclude Washington city
    if city != 'washington':
        earliest_year = df['Birth Year'].min()
        print('Earliest Year is: ',earliest_year)

        most_recent_year = df['Birth Year'].max()
        print('Most Recent Year is: ',most_recent_year)

        most_common_year = df['Birth Year'].mode()[0]
        print('Most Common Year is: ',most_common_year)
    else: print('Sorry, Wasington has no "Year of Birth" information.')
       
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def show_row_data(df):
    row=0
    while True:
        view_raw_data = input("Would you like to check the raw data? For 'Yes' enter 'Y' and for 'No' enter 'N'.\n").lower()
        #row = 0
        if view_raw_data == "y":
            print(df.iloc[row : row + 10])
            row += 10
        elif view_raw_data == "n":
            break
        else: #validate user input
            print("Invalid input! Please enter 'Y' or 'N'.")
            

def main():
    while True:
        city,month,day = get_filters()      
        df = load_data(city,month,day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        show_row_data(df)
        restart = input('\nWould you like to restart? Enter "Y" for yes or "N" for no.\n').lower()
        if restart.lower() != 'y':
            break
        
if __name__ == "__main__":
	main()