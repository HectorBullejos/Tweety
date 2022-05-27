import os
import tweepy
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import time
import pandas as pd

# interesting links
# https://developer.twitter.com/en/docs/twitter-api/v1/rules-and-filtering/search-operators

def read_words(dict_path_fn):
    abs_dict_path = dict_path_fn + "w.txt"
    file1 = open(abs_dict_path, 'r')
    Lines = file1.readlines()
    word_list_fn=[]
    for line in Lines:
        word_list_fn.append(line[:-1])
    return word_list_fn

def auth_data(dict_path_fn):
    abs_dict_path = dict_path_fn + "k.txt"
    file1 = open(abs_dict_path, 'r')
    Lines = file1.readlines()
    word_list_fn = []
    for line in Lines:
        word_list_fn.append(line[:-1])

    consumer_key = str(word_list_fn[0])
    consumer_secret = str(word_list_fn[1])
    access_token = str(word_list_fn[2])
    access_token_secret = str(word_list_fn[3])

    return consumer_key, consumer_secret, access_token, access_token_secret
    # rM59uTai8vEc1huzpe2MH0dkbtsHRDFOJw3u0Q2NiZ1KtJ81Ms apii secretkey
    # Bet32i0Tsd3bg5kLKsJfy5WFa api key


if __name__ == '__main__':
    cwd = str(os.getcwd())
    OUTPUT_PATH = os.path.join(cwd, "files/results/")
    DICT_PATH = os.path.join(cwd, "files/dict/")
    OATH_PATH = os.path.join(cwd, "files/Oath/red-grid-274219-06de9bec9848.json")
    word_list = read_words(DICT_PATH)
    con_key, con_sec, acc_tok, acc_sec = auth_data(DICT_PATH)


    auth = tweepy.OAuthHandler(con_key, con_sec)
    auth.set_access_token(acc_tok, acc_sec)

    api = tweepy.API(auth)
    results = []

    # use creds to create a client to interact with the Google Drive API

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name(OATH_PATH, scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("hoja")

    worksheet_1 = sheet.add_worksheet(title=str(datetime.date.today()), rows="1000", cols="4")

    for row in word_list:
        count = 0
        query = str(row) + " " + str("-filter:retweets")
        for tweet in tweepy.Cursor(api.search_tweets,
                                  q=query).items(5):

            count = count +1
            print(count,"keyword: ",str(row), "################################################# \ntweet:", tweet.text, "\nDate: ", tweet.created_at, "\nUser: ",tweet.user.name, "\nScreen_name:", tweet.user.screen_name)

            results.append([tweet.text, tweet.created_at, tweet.user.screen_name, str(row)])
            result = worksheet_1.append_row(
                [tweet.text, str(tweet.created_at), tweet.user.screen_name, str(row)])
            time.sleep(2)




    df = pd.DataFrame(results, columns=["text","date","user","keyword"])
    file_name = OUTPUT_PATH + str(datetime.date.today()) + ".csv"
    df.to_csv(file_name)



    # Create a column








    # fecha + 1
    # filtro de fecha
    # paginado

