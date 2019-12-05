# -*- coding: utf-8 -*-

"""=================================================
@Project -> File   ：tools -> kafka_utils.py
@IDE    : Pycharm
@Author : Qi Shuo
@Date   : 2019-11-22
@Intro  : KafKa tools
=================================================="""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from abc import abstractmethod
from kafka import KafkaConsumer, KafkaProducer
from concurrent.futures import ThreadPoolExecutor, as_completed


class KafkaConsumerRunner(object):
    __slots__ = ['bootstrap_servers', 'max_workers', 'group_id', 'topics',
                 'executor', 'poll_timeout_ms', 'poll_max_records']

    def __init__(self, bootstrap_servers, group_id, topics, max_workers,
                 poll_timeout_ms=200, poll_max_records=200):
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.topics = topics
        self.poll_timeout_ms = poll_timeout_ms
        self.poll_max_records = poll_max_records
        self.max_workers = max_workers
        self.executor = self._create_executor()

    def _create_consumer(self):
        consumer = KafkaConsumer(group_id=self.group_id, bootstrap_servers=self.bootstrap_servers)
        consumer.subscribe(topics=self.topics)
        return consumer

    def _create_executor(self):
        executor = ThreadPoolExecutor(max_workers=self.max_workers)
        return executor

    def _task(self, task_id):
        consumer = self._create_consumer()
        while True:
            msg_pack = consumer.poll(timeout_ms=self.poll_timeout_ms, max_records=self.poll_max_records)
            for tp, messages in msg_pack.items():
                print("task-{} process {} message.".format(task_id, len(messages)))
                for message in messages:
                    self.process_records(tp.topic, tp.partition, message.offset, message.key, message.value)

    @abstractmethod
    def process_records(self, topic, partition, offset, key, value):
        pass

    def run(self):
        all_task = [self.executor.submit(self._task, task_id) for task_id in range(self.max_workers)]
        for future in as_completed(all_task):
            result = future.result()
            print(result)


if __name__ == "__main__":
    pass
