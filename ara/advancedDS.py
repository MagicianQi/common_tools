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
    """Priority queue
    Elements push or pop by priority
    """

    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]


class LinkedListNode:

    def __init__(self, val):
        self.val = val
        self.next = None

    def __str__(self):
        return "LinkedListNode({})".format(self.val)


class LinkedList:

    def __init__(self):
        self.head = LinkedListNode("Head")
        self.tail = self.head

    def __str__(self):
        val_list = []
        ptr = self.head
        while ptr is not None:
            val_list.append(ptr.__str__())
            ptr = ptr.next
        return " -> ".join(val_list)

    def add_node(self, val):
        self.tail.next = LinkedListNode(val)
        self.tail = self.tail.next

    def delete_node(self, val):
        if val == self.head.val:
            return
        ptr_pre = self.head
        ptr = ptr_pre.next
        while ptr is not None:
            if ptr.val == val:
                ptr_pre.next = ptr.next
                del ptr
                break
            ptr = ptr.next
            ptr_pre = ptr_pre.next

    def sort(self, reverse=False):
        self.simple_sort(self.head.next, None)
        if reverse:
            self.reverse()

    def simple_sort(self, begin, end):
        if self.head.next is None or self.head.next.next is None:
            return
        if begin == end:
            return
        base = begin
        i = begin
        j = i.next
        while j != end:
            if j.val < base.val:
                i = i.next
                self._swap(i, j)
            j = j.next
        self._swap(base, i)
        self.simple_sort(base, i)
        self.simple_sort(i.next, end)

    @staticmethod
    def _swap(a, b):
        a.val, b.val = b.val, a.val

    def reverse(self):
        if self.head.next is None or self.head.next.next is None:
            return
        ptr_temp = None
        ptr_pre = self.head.next
        ptr_cur = self.head.next.next
        while ptr_cur is not None:
            ptr_pre.next = ptr_temp
            ptr_temp = ptr_pre
            ptr_pre = ptr_cur
            ptr_cur = ptr_cur.next
        ptr_pre.next = ptr_temp
        self.head.next = ptr_pre


if __name__ == "__main__":
    pass
