# -*- coding: utf-8 -*-

"""=================================================
@Project -> File   ：tools -> DOP.py
@IDE    : Pycharm
@Author : Qi Shuo
@Date   : 2019-10-10
@Intro  : Download Operations Tools
=================================================="""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


def download_images(image_urls, download_path, max_workers=1, data_slices=10):
    """
    Multi Threads download images
    :param image_urls: Image urls List
    :param download_path: Image download Path
    :param max_workers: Max Workers of Thread Pool
    :param data_slices: Number of data slices
    :return: None
    """
    def task(url_list, path, task_id):
        """
        Download images task
        :param url_list: List of image urls
        :param path: Image download Path
        :param task_id: ID of the current task
        :return: Status of Task
        """
        for url in url_list:
            try:
                response = requests.get(url)
                response = response.content
                with open(path + url.strip().split("/")[-1], 'wb') as f:
                    f.write(response)
            except Exception as e:
                print(e)
        return "{}:\t{}".format(task_id, "done")

    if download_path[-1] != "/":
        download_path += "/"
    executor = ThreadPoolExecutor(max_workers=max_workers)
    urls_list = [[] for _ in range(data_slices)]
    for i in range(len(image_urls)):
        urls_list[i % data_slices].append(image_urls[i])
    all_task = [executor.submit(task, urls_list[j], download_path, j) for j in range(len(urls_list))]
    for future in as_completed(all_task):
        result = future.result()
        print(result)


if __name__ == "__main__":
    pass
