from tweepy import Client
from dotenv import load_dotenv
from rich import print
import os

load_dotenv()

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_secret = os.getenv('ACCESS_SECRET')


def initialize_client() -> Client:
    return Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_secret
    )


if __name__ == '__main__':
    client = initialize_client()

    print(client.get_me().data.data)
