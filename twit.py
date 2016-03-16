import config  # file that contains my API token
import json
import oauth2 as oauth
import oauth2 as urllib


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
print req(url="https://api.twitter.com/1.1/statuses/user_timeline.json",
          method="GET",
          data={"screen_name": "dan_abramov"})


def follow_user(user_id=None, screen_name=None):
    if user_id:
        data = {"user_id": user_id}
    if screen_name:
        data = {"screen_name": screen_name}
    return req(
        url="https://api.twitter.com/1.1/friendships/create.json",
        method="POST",
        data=data)

# Follow user
print follow_user(screen_name="thatguyBG")


# Find users who retweeted my medium post
def find_retweet_users(tweet_id):
    data = {"count": 100, "id": tweet_id, "stringify_ids": "true"}
    response = req(
        url="https://api.twitter.com/1.1/statuses/retweeters/ids.json",
        method="GET",
        data=data)
    return json.loads(response)["ids"]

print find_retweet_users(tweet_id=707652131038351360)
