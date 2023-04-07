# Twitter_scrapper_capstone1
This is my first capstone project. I scrapped the data from twitter and displayed with the help of streamlit This program is a Twitter data scraper that scrapes tweets containing a specific keyword or hashtag within a given date range. 
The program uses the snscrape library to scrape Twitter data and the pandas library to store the data in a DataFrame. The scraped data is then stored in a MongoDB database using the pymongo library.

The program also includes a GUI created using the streamlit library. The GUI allows the user to input the keyword or hashtag to search, the start and end dates, and the number of tweets to scrape. 
When the user clicks the "Scrape the Data" button, the program scrapes the data and displays the scraped data in a table. The program also includes buttons to stores it in MongoDB, download the scraped data in CSV and JSON formats.

To use this program, you will need to have Python installed on your computer, along with the necessary libraries (snscrape, pandas, pymongo, and streamlit). You will also need to have access to a MongoDB server.

To run the program, open a terminal or command prompt in the directory where the program is saved and type the following command:

streamlit run twitter_data_scraper.py

This will launch the GUI in your web browser. Enter the necessary information in the input fields and click the "Scrape the Data" button to start scraping. The scraped data will be displayed in a table and can be downloaded in CSV and JSON formats using the download buttons.

Note: This program is for educational purposes only.
