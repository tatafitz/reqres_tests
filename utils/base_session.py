import logging

from requests import Session


class BaseSession(Session):
    def __init__(self, **kwargs):
        super().__init__()
        self.base_url = kwargs.get('base_url', None)

    def request(self, method, url, **kwargs):
        url = self.base_url + url

        response = super().request(method, url, **kwargs)
        logging.info(response.request)
        return response

