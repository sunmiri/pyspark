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
from pyspark.sql.types import StringType

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
        self.kin_streamname=kwargs.get("data.source.kinesis.streamname", "MyPySparkKinesis")
        self.kin_endurl=kwargs.get("data.source.kinesis.endpointurl", "https://kinesis.us-east-1.amazonaws.com")
        self.kin_region=kwargs.get("data.source.kinesis.region", "us-east-1")
        self.kin_start_pos=kwargs.get("data.source.kinesis.startingposition", InitialPositionInStream.TRIM_HORIZON) #LATEST
        #self.kin_aws_key=kwargs.get("data.source.kinesis.awsaccesskeyid", "")
        #self.kin_aws_scrt_key=kwargs.get("data.source.kinesis.awssecretkey", "")
        self.kin_chk_int=kwargs.get("data.source.kinesis.checkpointinterval", 1000)
        self.batch_dur_sec=kwargs.get("spark.stream.batch.duration.secs", 5)

        self.rsf_user=kwargs.get("sink.redshift_user","awsuser")
        self.rsf_pswd=kwargs.get("sink.redshift_pass",None)
        self.rsf_port=kwargs.get("sink.redshift_port",5439)
        self.rsf_table=kwargs.get("sink.redshift_table","dev")
        self.rsf_jdbc_url=kwargs.get("sink.redshift_jdbc_url",None)

        
        self.conf = SparkConf().setAppName(self.appname)
        print("__init__::self.conf:%s" % self.conf)

        self.sc = SparkContext(conf=self.conf)
        print("__init__::self.sc:%s" % self.sc)

        self.ssc = StreamingContext(self.sc, int(self.batch_dur_sec))
        print("__init__::self.ssc:%s" % (self.ssc))

        self.spark = SparkSession.builder.config(conf=self.conf).getOrCreate()
        print("__init__::self.spark:%s" % self.spark)
    
    #http://spark.apache.org/docs/latest/api/python/pyspark.streaming.html#pyspark.streaming.kinesis.KinesisUtils
    def initKinesis(self):
        print("initKinesis")
        self.kinesisStream = KinesisUtils.createStream(ssc=self.ssc, kinesisAppName=self.appname, streamName=self.kin_streamname, endpointUrl=self.kin_endurl, regionName=self.kin_region, initialPositionInStream=self.kin_start_pos, checkpointInterval=int(self.kin_chk_int))
        print("initKinesis::kinesisStream::", self.kinesisStream)

    def readData(self):
        print("readData")

        def processRDD(rdd):
            print("processRDD::rdd:%s" % (rdd))
            #rdd.foreach(lambda r: print(r))
            if rdd and rdd.isEmpty() == False:
                rddDF = self.spark.createDataFrame(rdd, StringType())
                rddDF.show()
                #https://docs.databricks.com/data/data-sources/aws/amazon-redshift.html
                #https://docs.aws.amazon.com/redshift/latest/mgmt/configure-jdbc-connection.html
                print("processRDD::writing records to AWS Redshift:u:%s,p:%s,t:%s,j:%s" % (self.rsf_user,self.rsf_pswd,self.rsf_table,self.rsf_jdbc_url))
                rddDF.write.mode("overwrite") \
                    .format("jdbc") \
                    .option("url", self.rsf_jdbc_url) \
                    .option("dbtable", self.rsf_table) \
                    .option("user", self.rsf_user) \
                    .option("password", self.rsf_pswd) \
                    .option("driver", "com.amazon.redshift.jdbc42.Driver") \
                    .save()
            
        self.kinesisStream.foreachRDD(lambda r: processRDD(r))
    
    #https://docs.aws.amazon.com/redshift/latest/dg/t_creating_database.html
    #create table testtable (message varchar(256));
    #insert into testtable values ('message');
    def writeToRedshift(self):
        print("")
        #Regular Table
        #aws redshift create-cluster --cluster-identifier demo --db-name demo --node-type dc1.large --cluster-type single-node --iam-roles "arn:aws:iam::YOUR-AWS-ACCOUNT:role/<redshift-iam-role>" \
        # --master-username master --master-user-password REDSHIFT-MASTER-PASSWORD --publicly-accessible --port 5439
        #External Table
        

    def start(self):
        self.readData()
        self.ssc.start()
        self.ssc.awaitTermination()
        
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
    app.initKinesis()
    app.start()