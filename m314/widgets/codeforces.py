import requests
from flask import Config
from flask import json
from redis import Redis

from m314.widget import Widget


class CodeforcesWidget(Widget):
    template = 'widgets/codeforces.html'
    redis_json = 'CODEFORCES_INFO_JSON'
    config_handle = 'CODEFORCES_HANDLE'
    def __init__(self, appcfg: Config, redis: Redis):
        super(CodeforcesWidget, self).__init__(appcfg, redis)
        assert self.config_handle in appcfg
        self.handle = appcfg[self.config_handle]
        self.template = 'widgets/codeforces.html'

    def get_info(self) -> dict:
        info_json = self.redis.get(self.redis_json)
        if info_json is None:
            info_json = requests.get("http://codeforces.com/api/user.info?handles={}").content
            self.redis.set(name=self.redis_json, value=info_json, ex=900)
        return json.loads(info_json)['result'][0]

