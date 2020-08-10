#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 11:21:19 2020

@author: sunilmiriyala
"""
#pyspark local run
"""
https://spark.apache.org/docs/latest/api/python/pyspark.sql.html
https://spark.apache.org/docs/latest/api/python/index.html

Run:
source /opt/codebase/PYTHON3/bin/activate 
cd <your-path>/PySpark/
sh ./setenv.sh
echo $SPARK_HOME
cd src/python/
$SPARK_HOME/bin/spark-submit pyspark-local.py
"""
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark import SparkContext, SparkConf
from jproperties import Properties
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType
from pyspark.sql.functions import col
from pyspark.sql.avro.functions import from_avro, to_avro

class PySparkLocal:
    def __init__(self, **kwargs):
        print("__init__::kwargs:%s" % kwargs)
        self.appname = kwargs.get("name", kwargs.get("spark.name", "PySpark-Local"))
        self.conf = SparkConf().setAppName(self.appname).setMaster(kwargs.get("master", kwargs.get("spark.master", "local")))
        print("__init__::self.conf:%s" % self.conf)
        self.sc = SparkContext(conf=self.conf)
        print("__init__::self.sc:%s" % self.sc)
        self.spark = SparkSession.builder.appName(self.appname).getOrCreate()
        print("__init__::self.spark:%s" % self.spark)
        self.spark.sparkContext.setLogLevel('WARN')
        #Local spark env (choices: local, cluster,..)
        self.file_location = kwargs.get("data.source.location")
        self.file_names = kwargs.get("data.source.files")
    
    def mytransform(self, r):
        print("transform::r:", r)

    def loadFiles(self):
        print("loadFiles")
        files = self.file_names.split(",")
        
        all_cust_rdd = self.spark.sparkContext.textFile(self.file_location + files[0])
        print("loadFiles::all_cust_rdd (RDD):%s" % all_cust_rdd)
        all_cust_rdd.foreach(lambda r: print("Row:", r))
        all_cust_fmap_rdd = all_cust_rdd.flatMap(lambda r: r.split(","))
        print("loadFiles::all_cust_fmap_rdd (RDD):%s" % all_cust_fmap_rdd)
        all_cust_fmap_rdd.foreach(lambda c: print("Cell:", c))

        all_cust_df = self.readFile(filePath=self.file_location + files[0])
        active_cust_df = all_cust_df.filter(all_cust_df.active == 1)
        
        all_apps_df = self.readFile(filePath=self.file_location + files[1])
        active_apps_df = all_apps_df.filter(all_apps_df.active == 1)

        all_cust_apps_df = self.readFile(filePath=self.file_location + files[2])
        active_cust_apps_df = all_cust_apps_df.filter(all_cust_apps_df.active == 1)

        cust_custapps_join_df = active_cust_df.join(other=active_cust_apps_df, on=(active_cust_df.id == active_cust_apps_df.cust_id), how='inner')
        print("loadFiles::cust_custapps_join_df:%s" % (cust_custapps_join_df))
        cust_custapps_join_df.printSchema()
        cust_custapps_join_df.show()

        all_apps_df.createOrReplaceTempView("ALL_APPS")
        all_cust_apps_df.createOrReplaceTempView("ALL_CUST_APPS")
        apps_custapps_join_df = self.spark.sql("select aa.name as app_name, aa.id as app_id, aca.cust_id as cust_id, aca.active as cust_app_active from ALL_APPS aa, ALL_CUST_APPS aca where aa.id == aca.app_id and aa.active == 1")
        print("loadFiles::apps_custapps_join_df:%s" % (apps_custapps_join_df))
        apps_custapps_join_df.printSchema()
        apps_custapps_join_df.show()
        print("loadFiles::groupBy::name:")
        apps_custapps_join_df.groupBy("app_name").count().show()
        
        apps_custapps_join_df.write.partitionBy("app_name").format("avro").mode("overwrite").save(self.file_location + "active_apps_custapps.avro")
        print("loadFiles::Successfully written to avro file")
        avro_oms_df = self.spark.read.format("avro").load(self.file_location + "active_apps_custapps.avro").where(col("app_name") == "OMS").show()
        print("loadFiles::avro_oms_df::", avro_oms_df)


    def readFile(self, filePath):
        print("readFile::**********************")
        print("readFile::filePath:%s" % filePath)
        df = self.spark.read.format('csv').options(header='true').options(inferSchema='true').load(filePath).cache()
        print("readFile::df:%s" % (df))
        df.printSchema()
        df.show()
        print("readFile::df.count:%s" % df.count())
        return df

if __name__ == '__main__':
    #More params
    #master = None, appName = None, sparkHome = None, pyFiles = None, 
    #environment = None, batchSize = 0, serializer = PickleSerializer(), 
    #conf = None, gateway = None, jsc = None, profiler_cls = <class 'pyspark.profiler.BasicProfiler'>
    
    kw = {}
    configs = Properties()
    with open('pyspark-csv.properties', 'rb') as config_file:
        configs.load(config_file)
    for p in configs:
        print("P:Name:%s, Val:%s" % (p, configs.get(p).data))
        kw[p] = configs.get(p).data
    print("configs::%s" % configs)
    psl = PySparkLocal(**kw)
    psl.loadFiles()