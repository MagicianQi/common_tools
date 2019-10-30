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
from contextlib import closing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed


def download_image_task(url_list, path, task_id):
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


class ProgressBar(object):
    """
    Progress bar chain
    """
    def __init__(self, title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "【%s】%s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        _info = self.info % (self.title, self.status,
                             self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)


def download_file(file_url, file_name, chunk_size=1024):
    """
    Follow the link to download the file
    :param file_url: The file link
    :param file_name: Download file name
    :param chunk_size: Download chunk size
    :return: None
    """
    with closing(requests.get(file_url, stream=True)) as response:
        content_size = int(response.headers['content-length'])  # 内容体总大小
        progress = ProgressBar(file_name, total=content_size,
                               unit="KB", chunk_size=chunk_size,
                               run_status="Downloading...", fin_status="Download complete")
        with open(file_name, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                progress.refresh(count=len(data))


if __name__ == "__main__":
    pass
