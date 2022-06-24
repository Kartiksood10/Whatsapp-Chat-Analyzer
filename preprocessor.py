import re
import pandas as pd


def preprocess(data):

    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    # pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'

    messages = re.split(pattern, data)[1:]  # list that contains only messages
    dates = re.findall(pattern, data)  # handles regex expressions and stores date and time in separate string

    # dataframe creation(df) using messages and dates

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert message_date type
    # df['date'].dt.year[0] extracts year of first date from date

    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')

    # df.rename(columns={'message_date': 'date'}, inplace=True)
    # df['year'] = df['date'].dt.year
    #
    # ans = len(str(df['date'].dt.year[0].item()))
    #
    # if ans == 4:
    #     df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y, %H:%M - ')
    #
    # if ans == 2:
    #     df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %H:%M - ')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # separating messages into users list and messages list eg. kartik: hello

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # username
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    # creating two new columns user and message in our dataframe

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # code for adding period to df which gives us one hour range of time for heatmap(8-9, 10-11 etc.)

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
