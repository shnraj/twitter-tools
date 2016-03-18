import config  # file that contains my API token
import json
import oauth2 as oauth
import oauth2 as urllib
import shelve


def req(url, method, data):
    consumer = oauth.Consumer(key=config.CONSUMER_KEY,
                              secret=config.CONSUMER_SECRET)
    access_token = oauth.Token(key=config.ACCESS_KEY,
                               secret=config.ACCESS_SECRET)
    client = oauth.Client(consumer, access_token)

    endpoint = url + "?" + urllib.urlencode(data)
    response, data = client.request(endpoint, method=method)

    return data

# Get user timeline
# print req(url="https://api.twitter.com/1.1/statuses/user_timeline.json",
#           method="GET",
#           data={"screen_name": "dan_abramov"})


def follow_user(user_id=None, screen_name=None):
    if user_id:
        data = {"user_id": user_id}
    if screen_name:
        data = {"screen_name": screen_name}
    response = req(
        url="https://api.twitter.com/1.1/friendships/create.json",
        method="POST",
        data=data)
    return json.loads(response)

# Follow user
# print follow_user(screen_name="thatguyBG")


def unfollow_user(user_id=None, screen_name=None):
    if user_id:
        data = {"user_id": user_id}
    if screen_name:
        data = {"screen_name": screen_name}
    response = req(
        url="https://api.twitter.com/1.1/friendships/destroy.json",
        method="POST",
        data=data)
    return json.loads(response)

# Unfollow user
# print unfollow_user(screen_name="thatguyBG")


# Find users who retweeted my medium post
def find_retweet_users(tweet_id):
    data = {"count": 100, "id": tweet_id, "stringify_ids": "true"}
    response = req(
        url="https://api.twitter.com/1.1/statuses/retweeters/ids.json",
        method="GET",
        data=data)
    return json.loads(response)["ids"]

# print find_retweet_users(tweet_id=707652131038351360)


def already_followed(user_id):
    if user_id:
        unfollowed_s = shelve.open('unfollowed')
        try:
            if str(user_id) in unfollowed_s.keys():
                return True
        finally:
            unfollowed_s.close()
    return False


# Follow all retweet users add them to a followed list
def follow_list(user_id_list):
    if user_id_list:
        for user_id in user_id_list:
            if not already_followed(user_id):
                response = follow_user(user_id=user_id)
                if "screen_name" in response:
                    s = shelve.open('followed')
                    try:
                        s[str(user_id)] = {'screen_name':
                                           response["screen_name"]}
                    finally:
                        s.close()
        return get_followed_list()


def get_followed_list():
    s = shelve.open('followed')
    try:
        followed_list = s.keys()
    finally:
        s.close()
    return followed_list

# print follow_list([441679284, 2421472752])


def get_unfollowed_list():
    s = shelve.open('unfollowed')
    try:
        unfollowed_list = s.keys()
    finally:
        s.close()
    return unfollowed_list


def delete_shelve(shelve_name):
    s = shelve.open(shelve_name)
    s.clear()


# Unfollow all users on followed list and add them to the ufollowed list
def unfollow_list():
    user_id_list = get_followed_list()
    if user_id_list:
        for user_id in user_id_list:
            response = unfollow_user(user_id=user_id)
            if "screen_name" in response:
                s = shelve.open('unfollowed')
                try:
                    s[str(user_id)] = {'screen_name': response["screen_name"]}
                finally:
                    s.close()
        delete_shelve("followed")
        return get_followed_list()
