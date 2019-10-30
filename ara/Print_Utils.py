#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""=================================================
@Project -> File   ：tools -> Print_Utils.py
@IDE    : Pycharm
@Author : Qi Shuo
@Date   : 2019-10-30
@Intro  : Print Tools
=================================================="""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tqdm import tqdm


class SimpleProgressBar(tqdm):

    def show_title(self, text):
        self.set_description_str(text)

    def show_content(self, text):
        self.set_postfix_str(text)


class TqdmUpTo(tqdm):
    """Alternative Class-based version of the above.
    Provides `update_to(n)` which uses `tqdm.update(delta_n)`.
    Inspired by [twine#242](https://github.com/pypa/twine/pull/242),
    [here](https://github.com/pypa/twine/commit/42e55e06).
    """

    def update_to(self, b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)
