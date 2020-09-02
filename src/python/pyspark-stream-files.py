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
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType
from pyspark.sql.functions import pandas_udf, PandasUDFType
import pandas as pd

#https://spark.apache.org/docs/latest/api/python/index.html
#http://spark.apache.org/docs/latest/streaming-kinesis-integration.html

#https://docs.aws.amazon.com/cli/latest/reference/kinesis/put-record.html
#aws kinesis put-record --stream-name pyspark-kinesis --cli-binary-format raw-in-base64-out --data "{'name':'sunil'}" --partition-key test

#https://aws.amazon.com/blogs/big-data/optimize-spark-streaming-to-efficiently-process-amazon-kinesis-streams/
class MyPySparkApp:
    def __init__(self, **kwargs):
        print("__init__::kwargs:%s" % kwargs)
        self.appname=kwargs.get("spark.name", "MyPySparkKinesis")
        self.master=kwargs.get("spark.master", "local")
        self.src_type=kwargs.get("data.source.type", "kinesis")
        self.src_format=kwargs.get("data.source.format", "json")
        self.batch_dur_sec=kwargs.get("spark.stream.batch.duration.secs", 5)

        self.src_folder = kwargs.get("source.folder")
        self.sink_folder = kwargs.get("sink.folder")
        
        self.conf = SparkConf().setAppName(self.appname)
        for e in kwargs:
            if e.find("conf.spark.") != -1:
                self.conf.set(e, kwargs.get(e))
        print("__init__::self.conf:%s" % self.conf)

        self.sc = SparkContext(conf=self.conf)
        print("__init__::self.sc:%s" % self.sc)

        self.ssc = StreamingContext(self.sc, int(self.batch_dur_sec))
        print("__init__::self.ssc:%s" % (self.ssc))

        self.spark = SparkSession.builder.config(conf=self.conf).getOrCreate()
        self.spark.sparkContext.setLogLevel("ERROR")
        print("__init__::self.spark:%s" % self.spark)

        self.data_schema = StructType([StructField('emp_number', IntegerType(), True), StructField('emp_name', StringType(), True), StructField('dept_name', StringType(), True), StructField('emp_id', IntegerType(), True), StructField('dept_id', IntegerType(), True)])
    
    #https://spark.apache.org/docs/latest/api/python/_modules/pyspark/sql/streaming.html#DataStreamWriter.format
    def startApp(self):
        print("startApp")

        def udfDistinctAggregation(key, pdf):
            print("udfDistinctAggregation::key:", key, ", pdf:", pdf)
            _pdf = pdf.groupby(['emp_name'])['dept_name'].apply(lambda x: ','.join(x)).reset_index()
            print("udfDistinctAggregation::_pdf1:", _pdf)
            #return pd.concat(_pdf[['emp_name']], _pdf[['dept_name']])
            _pdf = _pdf["emp_name"] + _pdf["dept_name"]
            df_combined = pd.DataFrame(_pdf, columns=['emp_name'])
            print("udfDistinctAggregation::df_combined:", df_combined)
            return df_combined
            

        #spark.udf.register("distAggUDF", udfDistinctAggregation,StringType())
        #distAggUDF = udf(lambda c: udfDistinctAggregation(c),StringType())
        csvDF = self.spark.readStream.csv(path=self.src_folder, schema=self.data_schema)
        #withColumn("agg_dept_name", (distAggUDF(col("dept_name"))))
        csvDF = csvDF.groupBy(col("emp_name")).applyInPandas(udfDistinctAggregation, schema="emp_name string")
        csvDF.writeStream.format("console").outputMode("append").start().awaitTermination()
        
    def start(self):
        self.startApp()
        
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