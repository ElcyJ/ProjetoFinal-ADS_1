import requests
from goodreads import client


class Api():

    def get_api():
        api = Api()
        api.url = "https://www.goodreads.com"
        api.key = "ULqHwkFZXEYUbBJIFS1YQ"
        api.secret = "HLcxP74rrl8hKBydMnQQ8t6FFuSR2N251Oq7znNqU"
        return api

    def get_client(self):
        return client.GoodreadsClient("ULqHwkFZXEYUbBJIFS1YQ","HLcxP74rrl8hKBydMnQQ8t6FFuSR2N251Oq7znNqU")

    def get_good_book(self, isbn):
        return requests.get(self.url+"/book/review_counts.json", params={"key": self.key, "isbns": isbn}).json()

    def get_good_book_id(self, isbn):
         return requests.get(self.url+"/book/review_counts.json", params={"key": self.key, "isbns": isbn}).json()['books'][0]['id']


    def get_good_book_cover(self, isbn):
        cg = self.get_client()
        return cg.book(self.get_good_book_id(isbn)).image_url

    def get_good_book_description(self, isbn):
        cg = self.get_client()
        return cg.book(self.get_good_book_id(isbn)).description



import requests
