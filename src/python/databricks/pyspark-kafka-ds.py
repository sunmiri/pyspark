#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 11:21:19 2020

@author: sunilmiriyala
"""
# https://spark.apache.org/docs/latest/api/python/index.html

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


# https://spark.apache.org/docs/latest/api/python/index.html

class KafkaDS:
    def __init__(self, **kwargs):
        print("__init__::kwargs:%s" % kwargs)
        self.appname = kwargs.get("spark.name", "MyPySparkKafka")
        self.master = kwargs.get("spark.master", "local")
        self.batch_dur_sec = kwargs.get("spark.stream.batch.duration.secs", 5)

        self.src_type = kwargs.get("data.source.type", "kafka")
        self.src_format = kwargs.get("data.source.format", "json")

        self.kfk_topic = kwargs.get("data.source.kafka.topic")
        self.kfk_topic_out = kwargs.get("data.sink.kafka.topic")

        self.kfk_brokers = kwargs.get("data.source.kafka.brokers")

        self.kfk_start = kwargs.get("data.source.kafka.startingposition", "earliest")
        self.kfk_chkpointint = kwargs.get("data.source.kafka.checkpointinterval", 10)

        self.kfk_auto_commit = kwargs.get("enable.auto.commit", True)
        self.sasl_protocol = kwargs.get("security.protocol", "SASL_SSL")
        self.sasl_mech = kwargs.get("sasl.mechanisms", "PLAIN")
        self.sasl_username = kwargs.get("sasl.username")
        self.sasl_password = kwargs.get("sasl.password")
        self.file_location = kwargs.get("data.lookup.location")
        self.file_names = kwargs.get("data.lookup.files")

        self.conf = SparkConf().setAppName(self.appname)
        print("__init__::self.conf:%s" % self.conf)

        self.ssc = StreamingContext(sc, int(self.batch_dur_sec))
        print("__init__::self.ssc:%s" % (self.ssc))

        self.spark = SparkSession.builder.config(conf=self.conf).getOrCreate()
        print("__init__::self.spark:%s" % self.spark)

    def readFile(self, filePath):
        print("readFile::**********************")
        print("readFile::filePath:%s" % filePath)
        df = self.spark.read.format('csv').options(header='true').options(inferSchema='true').load(filePath).cache()
        print("readFile::df:%s" % (df))
        df.printSchema()
        df.show()
        print("readFile::df.count:%s" % df.count())
        return df

    def readData(self):
        print("readData")
        files = self.file_names.split(",")
        lookupTableDF = self.readFile(filePath=self.file_location + files[0])
        #print("readData::all_cust_df:%s" % all_cust_df)
        lookupTableDF.show()
        lookupTableDF.describe()
        pdf_j = lookupTableDF.to_json(orient="records")
        print("readData::pdf_j:%s" % pdf_j)
        broadcast_dept = sc.broadcast(json.loads(pdf_j))
        print("readData::broadcast_dept:", broadcast_dept, broadcast_dept.value)

        # Read from Prop 'public.dept'
        # https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html
        kafka_data_df = self.spark.readStream.format("kafka") \
            .option("kafka.bootstrap.servers", self.kfk_brokers) \
            .option("group.id", self.appname) \
            .option("subscribe", self.kfk_topic) \
            .option("security.protocol", self.sasl_protocol) \
            .option("session.timeout.ms", 15000) \
            .option("startingOffsets", self.kfk_start) \
            .option("sasl.username", self.sasl_username) \
            .option("sasl.password", self.sasl_password) \
            .option("sasl.mechanisms", self.sasl_mech) \
            .load()

        print("readData::kafka_data_df(1)::", kafka_data_df)
        kafka_data_df = kafka_data_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
        print("readData::kafka_data_df(2)::", kafka_data_df)
        # kafka_data_df.show()
        # kafka_data_df.printSchema()
        kafka_data_df.writeStream.format("kafka")\
            .outputMode("append")\
            .option("checkpointLocation","/tmp/stream/pykafka_ss/")\
            .option("kafka.bootstrap.servers", self.kfk_brokers)\
            .option("topic", self.kfk_topic_out)\
            .start()\
            .awaitTermination()

    def start(self):
        self.readData()


if __name__ == '__main__':
    kw = {
        "spark.master": "local",
        "spark.name": "MyPySpark-Kafka",
        "spark.stream.batch.duration.secs": "10",
        "data.source.type": "kafka",
        "data.source.format": "json",
        "data.source.kafka.topic": "test_in",
        "data.sink.kafka.topic": "test_out",
        "data.source.kafka.group": "pyspark-kafka",
        "data.source.kafka.brokers": "pkc-lgwgm.eastus2.azure.confluent.cloud:9092",
        "data.source.kafka.startingposition": "earliest",
        "data.source.kafka.checkpointinterval": "5",
        "security.protocol": "SASL_SSL",
        "sasl.mechanisms": "PLAIN",
        "sasl.username": "PSBHOQHRR5Q3AIF5",
        "sasl.password": "your_password",
        "checkpointdir": "/tmp/stream/pykafka_ss/"
    }
    print("kw::%s" % kw)
    app = KafkaDS(**kw)
    app.start()

# FAQ
# 1
# 20/09/01 18:04:06 WARN NetworkClient: [Consumer clientId=consumer-spark-kafka-source-311c5061-6582-4a61-80f7-6296ced6ef3b-135981209-driver-0-1, groupId=spark-kafka-source-311c5061-6582-4a61-80f7-6296ced6ef3b-135981209-driver-0] Connection to node -2 (b-2.awskafkatutorialclust.bdn76x.c10.kafka.us-east-1.amazonaws.com/10.0.0.19:9092) could not be established. Broker may not be available.
# Fix: Start with Same Subnet and SecurityGroup as CLuster. EMR, MSK, VM all are on same SecurityGroup/Subnet/VPC

# 2
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