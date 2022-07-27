import logging 
from urllib.parse import urlparse


import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


# 절대 경로
import sys
sys.path.append('./')

from insta_crawler.mixins.account import AccountMixin
from insta_crawler.mixins.auth import LoginMixin
from insta_crawler.mixins.challenge import ChallengeResolveMixin
from insta_crawler.mixins.fbsearch import FbSearchMixin
from insta_crawler.mixins.highlight import HighlightMixin
from insta_crawler.mixins.hashtag import HashtagMixin
from instagrapi.mixins.password import PasswordMixin
from insta_crawler.mixins.private import PrivateRequestMixin
from insta_crawler.mixins.public import (
    ProfilePublicMixin,
    PublicRequestMixin,
    TopSearchesPublicMixin,
)
from insta_crawler.mixins.share import ShareMixin
from insta_crawler.mixins.user import UserMixin

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Client(
    PublicRequestMixin,
    ChallengeResolveMixin,
    PrivateRequestMixin,
    TopSearchesPublicMixin,
    ProfilePublicMixin,
    LoginMixin,
    ShareMixin,
    FbSearchMixin,
    HighlightMixin,
    UserMixin,
    AccountMixin,
    HashtagMixin,
    PasswordMixin
    ):
    proxy = None
    logger = logging.getLogger("insta_crawler")

    def __init__(self, settings: dict = {}, proxy: str = None, delay_range: list = None, **kwargs):
        super().__init__(**kwargs)
        self.settings = settings
        self.delay_range = delay_range
        self.set_proxy(proxy)
        self.init()

    def set_proxy(self, dsn: str):
        if dsn:
            assert isinstance(
                dsn, str
            ), f'Proxy must been string (URL), but now "{dsn}" ({type(dsn)})'
            self.proxy = dsn
            proxy_href = "{scheme}{href}".format(
                scheme="http://" if not urlparse(self.proxy).scheme else "",
                href=self.proxy,
            )
            self.public.proxies = self.private.proxies = {
                "http": proxy_href,
                "https": proxy_href,
            }
            return True
        self.public.proxies = self.private.proxies = {}
        return False
    