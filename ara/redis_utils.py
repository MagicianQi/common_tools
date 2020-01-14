# -*- coding: utf-8 -*-

"""=================================================
@Project -> File   ：tools -> redis_utils.py
@IDE    : Pycharm
@Author : Qi Shuo
@Date   : 2019-11-22
@Intro  : Redis tools
@Ref    : https://cloud.tencent.com/developer/article/1151834
=================================================="""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import redis


class RedisConnection(object):

    def __init__(self, host, port, password, db):
        self.redis = redis.StrictRedis(host=host,
                                       port=port,
                                       password=password,
                                       db=db)

    def all_keys(self, pattern=None):
        keys = []
        for key in self.redis.scan_iter(match=pattern):
            keys.append(key)
        return keys

    def flush_all(self):
        return self.redis.flushall()

    def get_val_by_key(self, key):
        return self.redis.get(key)

    def set_key(self, key, val):
        return self.redis.set(key, val)

    def close(self):
        self.redis.connection_pool.release()


class RedisPipeline(RedisConnection):

    def __init__(self, host, port, password, db):
        super(RedisPipeline, self).__init__(host, port, password, db)
        self.pipeline = self.redis.pipeline()

    def execute(self):
        self.pipeline.execute()


if __name__ == "__main__":
    pass
