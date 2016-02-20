import config  # file that contains my API token
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

# Follow user
print req(url="https://api.twitter.com/1.1/friendships/create.json",
          method="POST",
          data={"screen_name": "thatguyBG"})
