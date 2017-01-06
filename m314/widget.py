from abc import ABCMeta, abstractmethod

from flask import Config
from redis import Redis


class Widget(metaclass=ABCMeta):

    def __init__(self, appcfg: Config, redis: Redis):
        self.appcfg = appcfg
        self.redis = redis

    @abstractmethod
    def render(self) -> str:
        pass
