# -*- coding: utf-8 -*-

"""=================================================
@Project -> File   ：tools -> Download_Utils.py
@IDE    : Pycharm
@Author : Qi Shuo
@Date   : 2019-10-10
@Intro  : Download Operations Tools
=================================================="""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import requests
import urllib.request

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

from ara.Print_Utils import TqdmUpTo, SimpleProgressBar
from ara.File_Utils import read_text_file_to_list


def download_image_task(url_list, path, task_id):
    """
    Download images task
    :param url_list: List of image urls
    :param path: Image download Path
    :param task_id: ID of the current task
    :return: Status of Task
    """
    url_list = SimpleProgressBar(url_list)
    for url in url_list:
        url_list.show_title("task - {}".format(task_id))
        try:
            response = requests.get("http://" + url)
            response = response.content
            with open(path + url.strip().split("/")[-1], 'wb') as f:
                f.write(response)
        except Exception as e:
            print(e)
    return "task-{}: {}".format(task_id, "done")


def download_images(image_urls, download_path, max_workers=1, data_slices=10):
    """
    Multi Threads download images
    :param image_urls: Image urls List
    :param download_path: Image download Path
    :param max_workers: Max Workers of Thread Pool
    :param data_slices: Number of data slices
    :return: None
    """
    if download_path[-1] != "/":
        download_path += "/"
    executor = ThreadPoolExecutor(max_workers=max_workers)
    # executor = ProcessPoolExecutor(max_workers=max_workers) # Switching to multiple processes
    urls_list = [[] for _ in range(data_slices)]
    for i in range(len(image_urls)):
        urls_list[i % data_slices].append(image_urls[i])
    all_task = [executor.submit(download_image_task, urls_list[j], download_path, j) for j in range(len(urls_list))]
    for future in as_completed(all_task):
        result = future.result()
        print(result)


def download_file(file_url, save_path, unit_divisor=1024):
    """
    Follow the link to download the file
    :param unit_divisor: Unit
    :param file_url: The file link
    :param save_path: Download file name
    :return: None
    """
    with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=unit_divisor, miniters=1,
                  desc=file_url.replace('/', ' ').split()[-1]) as t:
        urllib.request.urlretrieve(file_url, filename=save_path, reporthook=t.update_to,
                                   data=None)


if __name__ == "__main__":
    urls = read_text_file_to_list("./result/image.urls", separator="\t")
    urls = [x[0] for x in urls]
    download_images(urls, "./result", max_workers=5, data_slices=5)
