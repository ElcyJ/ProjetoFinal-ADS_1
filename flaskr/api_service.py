import requests


class Api():

    def get_api():
        api = Api()
        api.url = "https://www.goodreads.com/"
        api.key = "ULqHwkFZXEYUbBJIFS1YQ"
        return api


    def get_good_book(self, isbn):
        return requests.get(self.url+"/book/review_counts.json", params={"key": self.key, "isbns": isbn}).json()

    
