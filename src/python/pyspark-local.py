#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 11:21:19 2020

@author: sunilmiriyala
"""
#pyspark local run
"""
Run:
source /opt/codebase/PYTHON3/bin/activate 
cd <your-path>/PySpark/
sh ./setenv.sh
echo $SPARK_HOME
cd src/python/
$SPARK_HOME/bin/spark-submit pyspark-local.py
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark import SparkContext, SparkConf

class PySparkLocal:
    def __init__(self, **kwargs):
        print("__init__::kwargs:%s" % kwargs)
        #self.sc = SparkContext(kwargs.get("master", "local"), kwargs.get("name", "PySpark-Local"))
        self.conf = SparkConf().setAppName(kwargs.get("name", "PySpark-Local")).setMaster(kwargs.get("master", "local"))
        print("__init__::self.conf:%s" % self.conf)
        self.sc = SparkContext(conf=self.conf)
        print("__init__::self.sc:%s" % self.sc)
        self.spark = SparkSession.builder.appName(kwargs.get("name", "PySpark-Local")).getOrCreate()
        print("__init__::self.spark:%s" % self.spark)
        self.spark.sparkContext.setLogLevel('WARN')
        #Local spark env (choices: local, cluster,..)
        #Name of my application
    
    def readFile(self, filePath):
        print("readFile::filePath:%s" % filePath)
        logData = self.sc.textFile(filePath).cache() #one record per line in a file
        print("readFile::logData:%s" % logData)
        #add up the sizes of all the lines using the map and reduce
        #wordCounts = logData.map(lambda s: len(s)).reduce(lambda a, b: a + b)
        #print("readFile::wordCounts:%s" % wordCounts)
        lineLengths = logData.map(lambda s: len(s))
        lineLengths.persist() #saved in memory
        totalLength = lineLengths.reduce(lambda a, b: a + b) #an action
        print("readFile::totalLength:%s" % totalLength)

        #Cache: a cluster-wide in-memory cache
        logDataDF = self.spark.read.text(filePath).cache()
        print("readFile::logDataDF:%s" % logDataDF)
        print("readFile::logDataDF.count:%s" % logDataDF.count())
        print("readFile::logDataDF.first:%s" % logDataDF.first())
        logDataDFFiltered = logDataDF.filter(logDataDF.value.contains("Spark"))
        print("readFile::logDataDFFiltered:%s" % logDataDFFiltered)
        print("readFile::logDataDFFiltered.count():%s" % logDataDFFiltered.count())
        #Explode: transform a Dataset of lines to a Dataset of words
        wordCounts = logDataDF.select(explode(split(logDataDF.value, "\s+")).alias("word")).groupBy("word").count()
        print("readFile::wordCounts:%s" % wordCounts)
        wordCounts.collect()
        print("readFile::wordCounts::", wordCounts.head())

if __name__ == '__main__':
    #More params
    #master = None, appName = None, sparkHome = None, pyFiles = None, 
    #environment = None, batchSize = 0, serializer = PickleSerializer(), 
    #conf = None, gateway = None, jsc = None, profiler_cls = <class 'pyspark.profiler.BasicProfiler'>
    kw = {"name":"MyPySpark-Local-Test1", "master": "local"}
    psl = PySparkLocal(**kw)
    psl.readFile(filePath="/Users/sunilmiriyala/CirrusSS/A-Cloud/Training/PySpark/src/python/README.md")
