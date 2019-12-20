# -*- coding: utf-8 -*-

"""=================================================
@Project -> File   ：tools -> advancedDS.py
@IDE    : Pycharm
@Author : Qi Shuo
@Date   : 2019-12-20
@Intro  : Advanced data structure
=================================================="""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import heapq


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]


if __name__ == "__main__":
    pass
