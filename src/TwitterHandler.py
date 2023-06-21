from getpass import getpass
import json
from pathlib import Path
import os
from typing import  Dict

import tweepy

from src.encryptor import get_encrypted_meta_data, load_key, pgpy_decrypt
from src.ImageBuilder import ClippingData
    
class TwitterHandler:
    def __init__(self, pwd: str, key: str = "TWITTER") -> None:
        self.current_path = Path(os.path.realpath(os.path.dirname(__file__)))
        self.get_client(pwd, key)

    def get_client(self, pwd, key) -> None:
        api_data_encrypted: Dict[str,str] = get_encrypted_meta_data(str(self.current_path))
        key_file = load_key(str(self.current_path))

        with key_file.unlock(pwd):
            decrypted = pgpy_decrypt(key_file, api_data_encrypted).replace('\'', '\"')
            data = json.loads(decrypted)[key]

        auth = tweepy.OAuthHandler(consumer_key=data["Key"], consumer_secret=data["Secret"])
        auth.set_access_token(key=data["Other_fields"]["access_token"], secret=data["Other_fields"]["access_token_secret"])
                              
        self.api = tweepy.API(auth)

        self.client = tweepy.Client(consumer_key=data["Key"], consumer_secret=data["Secret"], 
                                    access_token=data["Other_fields"]["access_token"], access_token_secret=data["Other_fields"]["access_token_secret"])

    def tweet_image(self, clipping_data: ClippingData) -> None:

        book_title, _ = clipping_data.storedClipping

        # Upload media to Twitter APIv1.1
        media = self.api.media_upload(filename="Quote", file= clipping_data.get_image_bytecode())

        # tweet
        self.client.create_tweet(media_ids=[media.media_id_string], text=f"{book_title}")


if __name__ == "__main__":
    pwd = getpass("provide password for pk:")
    executor = TwitterHandler(pwd)