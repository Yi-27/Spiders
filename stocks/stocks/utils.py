# -*- coding: utf-8 -*-
# 一些工具方法
from .settings import *
import time
import redis
import pymongo
from selenium import webdriver
from pykafka import KafkaClient
import random

class SeleniumUtils(object):
    
    @classmethod
    def get_selenium(cls):
        """返回一个无窗口的selenium的driver"""
        options = webdriver.ChromeOptions()
        options.add_argument("headless")  # 无窗口
        return webdriver.Chrome(executable_path="./chromedriver.exe", options=options)


# 数据库相关的工具类
class DBUtils(object):
    
    @classmethod
    def get_redis(cls, *args, **kwargs):
        """返回一个redis连接"""
        return redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 连接Redis
    
    @classmethod
    def get_mongo(cls, *args, **kwargs):
        """返回一个redis连接"""
        return pymongo.MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)
  

# kafka相关的工具类
class KafkaUtils(object):

    def __init__(self):
        # kafka连接池
        self.client = self.get_kafka()
    
    def get_kafka(self, *args, **kwargs):
        """创建一个kafka连接，注意这个kafka可能是个集群"""
        client = KafkaClient(hosts=",".join(KAFKA_HOSTS),
                    zookeeper_hosts=",".join(ZOOKEEPER_HOSTS))
        return client
    
    def get_topic(self, topic_name):
        """获取指定的topic连接"""
        # 判断连接是否可用
        # 返回一个同步生产者
        return self.client.topics[topic_name]
    
    def get_sync_producer(self, topic_name):
        """返回一个同步生产者"""
        topic = self.get_topic(topic_name)
        return topic.get_sync_producer()
    
    def get_producer(self, topic_name):
        """返回一个异步生产者"""
        topic = self.get_topic(topic_name)
        return topic.get_producer(sync=False,
                                        delivery_reports=True,
                                        partitioner=lambda pid, key: pid[0])
    
    def get_simple_consumer(self, topic_name):
        """返回一个普通的消费者，从头读到尾"""
        topic = self.get_topic(topic_name)
        return topic.get_simple_consumer()