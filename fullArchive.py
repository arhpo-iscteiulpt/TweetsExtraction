# For sending GET requests from the API
import requests
# For saving access tokens and for file management when creating and adding to the dataset
import os
# For dealing with json responses we receive from the API
import json
# To add wait time between requests
import time

os.environ['TOKEN'] = 'YOUR BEARER TOKEN'


def auth():
    return os.getenv('TOKEN')


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def create_url(keyword, start_date, end_date, max_results):
    search_url = "https://api.twitter.com/2/tweets/search/all"  # Change to the endpoint you want to collect data from

    # change params based on the endpoint you are using
    query_params = {'query': keyword,
                    'start_time': start_date,
                    'end_time': end_date,
                    'max_results': max_results,
                    'expansions': 'author_id,in_reply_to_user_id,geo.place_id,entities.mentions.username',
                    'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,'
                                    'public_metrics,referenced_tweets,reply_settings,source',
                    'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                    'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                    'next_token': {}}
    return (search_url, query_params)


def connect_to_endpoint(url, headers, params, next_token=None):
    params['next_token'] = next_token  # params object received from create_url function
    response = requests.request("GET", url, headers=headers, params=params)
    # print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def get_all(user, max_results, start_time, end_time):
    # Inputs for the request
    bearer_token = auth()
    headers = create_headers(bearer_token)
    keyword = "from:"+user

    url = create_url(keyword, start_time, end_time, max_results)
    json_response = connect_to_endpoint(url[0], headers, url[1])

    tweets = json_response['data']
    users = []
    places = []

    if 'includes' in json_response:
        if 'users' in json_response['includes']:
            users = json_response['includes']['users']
        if 'places' in json_response['includes']:
            places = json_response['includes']['places']

    if 'next_token' in json_response['meta']:
        next_token = json_response['meta']['next_token']
        print(next_token)
        count = json_response['meta']['result_count']
        print(count)

        while 'next_token' in json_response['meta']:
            next_token = json_response['meta']['next_token']
            json_response = connect_to_endpoint(url[0], headers, url[1], next_token)
            print(next_token)
            tweets.extend(json_response['data'])

            if 'includes' in json_response:
                if 'users' in json_response['includes']:
                    users.extend(json_response['includes']['users'])
                if 'places' in json_response['includes']:
                    places.extend(json_response['includes']['places'])

            count = count + json_response['meta']['result_count']
            print(count)
            time.sleep(5)

    return tweets, users, places
