# Twitter Timeline Extraction (API v2)
A script to create an endpoint with Twitter API Get v2, extract tweets from a user and save them into a excel file (.xlsx). 

Based on a *Towards Data Science* tutorial, access [here](https://towardsdatascience.com/an-extensive-guide-to-collecting-tweets-from-twitter-api-v2-for-academic-research-using-python-3-518fcb71df2a) (last accessed date 25/06/2021)

**Note:** You need Academic Research Access, know more [here](https://developer.twitter.com/en/products/twitter-api/academic-research)

## Content
- *fullArchive.py*, to create an endpoint and perform the search get.
- *excel_handler.py*, creates a workbook with worksheets for the search response.
- *main.py*, an usage example of the previous files 

## Authentication and Endpoint Creation
For the authentication you will need a **Bearer Token** from the Academic Research Access of the Twitter API v2.

The endpoint creation has two parts:
1. First the creation of a search url with the search params ```def create_url```, know more about how to change the url [here](https://developer.twitter.com/en/docs/twitter-api/tweets/search/quick-start/recent-search);
2. The connection to the endpoint using the previous url ```def connect_to_endpoin```.

## Extract a Twitter Timeline
The function ```def get_all(user, max_results, start_time, end_time)``` calls the previous functions to create the endpoint, and its inputs are:
- **user**, the Twitter username to extract timeline tweets;
- **max_results**, in this new API version, the search works with pagination, and each page has a maximum value of results that you can specify here (it can be a value between 1 and 500);
- **start_time** and **end_time** to specify the search time wanted.

When the endpoint connection is achieved it starts the search and it provides a json response for each page. The response in a json format like the following structure:
```
{ 
  "data": [...],
  "includes": {
    "places": [...],
    "users": [...]
  }
  "meta": {
    "newest_id": "...",
    "next_token": "...",
    "oldest_id": "...",
    "result_count": 100
    }
}
```
In the **data** is a list of tweets resulting from the search, in **includes** are the mentioned users and places, and in **meta** is the relevant information for the pagination. The function ```def get_all``` returns three lists: *data_list*, *users_list* and *places_list*. 

In the **meta** is the *next_token* value which gives access to the next page due to the pagination, and each page has a maximum vale of results has mentioned. 

## Excel Handler
In the file *excel_handler.py* are implemented the following three functions:
- ```def create_workbook(filename)```, to create an excel workbook to be saved at "filename" location;
- ```def worksheet_timeline(data_list, workbook, username)```, it creates a worksheet with the name username in the workbook and fills it with the data_list (the tweets from the timeline);
- ```def worksheet_users(user_list, workbook, sheetname)```, it creates a worksheet with the name sheetname in the workbook and fills it with the user_list (the users mentioned in the tweets timeline);
- ```def worksheet_places(places_list, workbook, sheetname)```, it creates a worksheet with the name sheetname in the workbook and fills it with the places_list (the places from the tweets' geolocation information);

## How to use
In the file *main.py* there is a example of a possible usage:
