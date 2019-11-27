# -*- coding: utf-8 -*-

"""=================================================
@Project -> File   ：tools -> redis_utils.py
@IDE    : Pycharm
@Author : Qi Shuo
@Date   : 2019-11-22
@Intro  : Redis tools
=================================================="""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import redis


class RedisConnection:

    def __init__(self, host, port, password, db):
        self.redis = redis.StrictRedis(host=host,
                                       port=port,
                                       password=password,
                                       db=db)
        self.pipeline = self.redis.pipeline()
