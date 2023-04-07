# importing necessary libraries
import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import pymongo
from datetime import datetime,timedelta
# Scrapping twitter data
def scrape_data(keyword,start_date,end_date,tweet_count):
    scraped_data = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(
        f'{keyword} since:{start_date} until:{end_date}').get_items()):
        if i >= tweet_count:
            break
        #Adding scraped data into a empty list
        scraped_data.append([tweet.date, tweet.id, tweet.url, tweet.content,
        tweet.user.username, tweet.replyCount, tweet.retweetCount, tweet.likeCount,
        tweet.lang, tweet.source])
    # Converting the list to dataframe
    df = pd.DataFrame(scraped_data, columns=["Date","ID","URL","Content",
                                             "User Name","Reply count",
                                             "Retweet count","Like count","Language",
                                             "Source"
                                             ])
    return df

# storing the data in to mongodb
def store_data_mongodb (data, keyword, start_date):
    #connecting to server
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    # Creating database
    db = client["twitter_data"]
    # creating collection with keyword
    collection = db["scraped_data"]
    Dict_data = data.to_dict("records")
    my_doc = [{"Scraped word" : keyword, "Scraped date":str(start_date), "Scraped data":Dict_data}]
    # Inserting the data
    collection.insert_many (my_doc)
    
  
# Create GUI
def create_gui():
    st.title("Twitter scraper")
    keyword = st.text_input("Enter a keyword or hashtag to scrape")
    start_date = st.date_input("Select the start date:")
    end_date = st.date_input("Select the end date:")
    tweet_count = st.number_input("Enter the number of tweets to scrap:", value=100)

    # converting the date in preferred formate
    start_date_str = datetime.strftime(start_date, "%Y-%m-%d")
    end_date_str = datetime.strftime(end_date + timedelta(days=1), "%Y-%m-%d")
    
    # Defining calling function
    def submit():
        data = scrape_data (keyword,start_date_str,end_date_str,tweet_count)
        return data
    def upload():
        data = submit()
        store_data_mongodb (data, keyword, start_date)
        return st.write("Uploaded sucessfully!")
    
    # initiating session state
   
    if "button1" not in st.session_state:
        st.session_state["button1"] = False

    if "button2" not in st.session_state:
        st.session_state["button2"] = False


    if st.button("Submit",key="Button1"):
        st.session_state["button1"] = not st.session_state["button1"]
        
        # Calling the scraping function
        data = submit()
        
        # Display the scraped data
        st.write(data)

    # Uploading to databse
    if st.session_state["button1"]:
        if st.button("Upload to database",key="Button2"):
            st.session_state["button2"] = not st.session_state["button2"]
            upload()
            
        # calling data
        data = submit()
        # converting data as csv
        csv = convert_data(data,"csv")

        # creating download buttons for
        st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='Twitter data.csv',
        mime='text/csv',
        )
        # concerting data as json
        json = convert_data(data,"json")

        # creating download buttons for json
        st.download_button(
        label="Download data as json",
        data=json,
        file_name='Twitter data.json',
        mime='text/json',
        )
    
# converting data 
def convert_data(data,type):
    if type == "csv":
        return data.to_csv(index = False).encode('utf-8')
    elif type == "json":
        return data.to_json(indent = 4)

create_gui()