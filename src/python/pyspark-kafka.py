#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 11:21:19 2020

@author: sunilmiriyala
"""
#https://spark.apache.org/docs/latest/api/python/index.html

import sys
import pyspark
from pyspark.streaming.kinesis import KinesisUtils, InitialPositionInStream
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from jproperties import Properties
from pyspark.storagelevel import StorageLevel 
from pyspark.sql.types import Row
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.functions import explode
from pyspark.sql.functions import split

#https://spark.apache.org/docs/latest/api/python/index.html

class MyPySparkApp:
    def __init__(self, **kwargs):
        print("__init__::kwargs:%s" % kwargs)
        self.appname=kwargs.get("spark.name", "MyPySparkKafka")
        self.master=kwargs.get("spark.master", "local")
        self.batch_dur_sec=kwargs.get("spark.stream.batch.duration.secs", 5)
        
        self.src_type=kwargs.get("data.source.type", "kafka")
        self.src_format=kwargs.get("data.source.format", "json")

        self.kfk_topic=kwargs.get("data.source.kafka.topic")
        self.kfk_brokers=kwargs.get("data.source.kafka.brokers")
        self.kfk_zookeeper=kwargs.get("data.source.kafka.zookeeper")
        self.kfk_region=kwargs.get("data.source.kafka.region", "us-east-1")
        self.kfk_start=kwargs.get("data.source.kafka.startingposition", "latest")
        self.kfk_chkpointint=kwargs.get("data.source.kafka.checkpointinterval", 10)
        self.kfk_auto_commit=kwargs.get("enable.auto.commit", True)
        
        self.conf = SparkConf().setAppName(self.appname)
        print("__init__::self.conf:%s" % self.conf)

        self.sc = SparkContext(conf=self.conf)
        print("__init__::self.sc:%s" % self.sc)

        self.ssc = StreamingContext(self.sc, int(self.batch_dur_sec))
        print("__init__::self.ssc:%s" % (self.ssc))

        self.spark = SparkSession.builder.config(conf=self.conf).getOrCreate()
        print("__init__::self.spark:%s" % self.spark)
    

    def readData(self):
        print("readData")
        #Read from Prop 'public.dept'
        #https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html
        kafka_data_df = self.spark.readStream.format("kafka") \
            .option("kafka.bootstrap.servers", self.kfk_brokers) \
            .option("subscribe", self.kfk_topic) \
            .option("startingOffsets", "earliest") \
            .load()
            #.option("group.id", self.appname) \
            #.option("startingOffsets", self.kfk_start) \
            #.option("auto.offset.reset", self.kfk_start) \
            #.option("enable.auto.commit", self.kfk_auto_commit) \
        print("readData::kafka_data_df(1)::", kafka_data_df)
        kafka_data_df = kafka_data_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
        print("readData::kafka_data_df(2)::", kafka_data_df)
        #kafka_data_df.show()
        kafka_data_df.printSchema()
        kafka_data_df.writeStream.format("console").outputMode("append").start().awaitTermination()
        
    
    def start(self):
        self.readData()
        
if __name__ == '__main__':
    import json
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", help="Properties File", dest='prop', required=True)
    args = parser.parse_args()
    kw = {}
    configs = Properties()
    with open(args.prop, 'rb') as config_file:
        configs.load(config_file)
    for p in configs:
        print("P:Name:%s, Val:%s" % (p, configs.get(p).data))
        kw[p] = configs.get(p).data
    print("configs::%s" % configs)
    app = MyPySparkApp(**kw)
    app.start()

#FAQ
#1
#20/09/01 18:04:06 WARN NetworkClient: [Consumer clientId=consumer-spark-kafka-source-311c5061-6582-4a61-80f7-6296ced6ef3b-135981209-driver-0-1, groupId=spark-kafka-source-311c5061-6582-4a61-80f7-6296ced6ef3b-135981209-driver-0] Connection to node -2 (b-2.awskafkatutorialclust.bdn76x.c10.kafka.us-east-1.amazonaws.com/10.0.0.19:9092) could not be established. Broker may not be available.
#Fix: Start with Same Subnet and SecurityGroup as CLuster. EMR, MSK, VM all are on same SecurityGroup/Subnet/VPC

#2
"""
readData::kafka_data_df(1):: DataFrame[key: binary, value: binary, topic: string, partition: int, offset: bigint, timestamp: timestamp, timestampType: int]
readData::kafka_data_df(2):: DataFrame[key: string, value: string]
Traceback (most recent call last):
  File "/usr/lib/spark/python/lib/pyspark.zip/pyspark/sql/utils.py", line 63, in deco
  File "/usr/lib/spark/python/lib/py4j-0.10.7-src.zip/py4j/protocol.py", line 328, in get_return_value
py4j.protocol.Py4JJavaError: An error occurred while calling o91.awaitTermination.
: org.apache.spark.sql.streaming.StreamingQueryException: Bad return type
Exception Details:
  Location:
"""