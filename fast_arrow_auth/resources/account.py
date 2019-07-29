class Account(object):
    @classmethod
    def all(cls, client):
        request_url = "https://api.robinhood.com/accounts/"
        data = client.get(request_url)
        results = data["results"]
        while data["next"]:
            data = client.get(data["next"])
            results.extend(data["results"])
        return results

    @classmethod
    def all_urls(cls, client):
        accounts = cls.all(client)
        urls = [account["url"] for account in accounts]
        return urls
