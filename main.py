import os
import tweepy
from tweepy import Client, StreamingClient
from dotenv import load_dotenv
from rich import print

load_dotenv()

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_secret = os.getenv('ACCESS_SECRET')
bearer_token = os.getenv('BEARER_TOKEN')


class OshiTweetStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        tweet_data = tweet.data

        if tweet_data['text'].__contains__('https://t.co/'):
            client.retweet(tweet_id=tweet_data['id'], user_auth=True)

        client.like(tweet_id=tweet_data['id'], user_auth=True)
        print(tweet_data)

    def on_disconnect(self):
        rules = self.get_rules().data
        ids = list(map(lambda rule: rule.id, rules))

        self.delete_rules(ids=ids)

        print("Disconnected, clearing rules...")


def initialize_client() -> Client:
    return Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_secret,
        wait_on_rate_limit=True
    )


def initialize_stream() -> StreamingClient:
    return OshiTweetStream(
        bearer_token=bearer_token,
        wait_on_rate_limit=True
    )


if __name__ == '__main__':
    client = initialize_client()
    streaming_client = initialize_stream()

    oshi_account = client.get_user(username='N_ShaniJKT48', user_auth=True)

    rule_query = 'from:N_ShaniJKT48 -is:reply -is:retweet'
    rule_ids = list(map(lambda rule: rule.id, streaming_client.get_rules().data))

    streaming_client.delete_rules(ids=rule_ids)
    streaming_client.add_rules(tweepy.StreamRule(rule_query))

    streaming_client.filter(threaded=True)
