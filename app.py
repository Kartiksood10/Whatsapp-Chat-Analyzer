import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    # st.text(data) prints all messages in chat
    # st.dataframe(df)  # creates a dataframe of the chat according to preprocessed df


    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall") # add section Overall at 0th index

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"): # condition runs when Show Analysis is clicked on streamlit

        # Stats area

        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # monthly timeline - stats about most chats on which months etc.

        st.title("Monthly timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        # we need a graph between message and time
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline

        st.title("Daily timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity map - gives most busy day and month

        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy day")
            busy_day = helper.weekly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # heatmap code

        st.title("Weekly Activity heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest users in the group(Group level)

        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            # graph representation of frequent users
            with col1:
                ax.bar(x.index, x.values, color = 'red')  # ax.bar takes x value and y value
                plt.xticks(rotation='vertical')  # xticks converts x axis values to vertical
                # pyplot prints the required graph
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # WordCloud - gives a pictorial representation of most used words with the most frequent having largest size
        st.title('WordCloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words

        st.title('Frequently Used Words')
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()
        # df[0] and df[1] are messages and their frequency respectively
        ax.barh(most_common_df[0], most_common_df[1])  # barh gives horizontal bar graph
        plt.xticks(rotation='vertical')

        st.pyplot(fig)

        # emoji analysis

        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)







