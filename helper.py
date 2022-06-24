from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()


def fetch_stats(selected_user,df):

    # if condition for when we want data of a particular person in group chat
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    # fetching number of messages
    # .shape[0] returns total number of data present in dataframe

    num_messages = df.shape[0]

    # fetching number of words
    # all words in message are added to words list through .extend, .split makes string into a list with each word a list item
    # we will return len(words) to get total number of words used

    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetching number of media files shared

    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetching number of links shared

    links = []
    for message in df['message']:
        # finding urls using URLExtract
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    # .head() returns top 5 rows of that particular row/column

    x = df['user'].value_counts().head()
    # finding percentage of messages sent by a user to 2 decimal places and changing value names in table

    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'Name', 'user': 'Percent'})
    return x, df


def create_wordcloud(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    # creating function to remove some stop words in our wordcloud too

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):

    # txt files contains a list of stop words in hinglish that we need to omit from our most common words
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    # removing group notifications(like person added, icon changed) and media omitted message from most common words in temp variable

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split(): # converting all words to lower case and accessing each word through .split()
            if word not in stop_words:
                words.append(word) # .append added word to the existing list

    # creating dataframe with count of frequent words(top 20)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user, df):

    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI_ENGLISH])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # count of number of messages in each month grouped according to month no. and name with year in df
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    # aim is to create a graph between number of messages and month-year(for eg. july-2019 91 messages)
    # time has list of all months-year

    time = []
    for i in range(timeline.shape[0]):
        # adds month-year to time list
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline


def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def weekly_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap













