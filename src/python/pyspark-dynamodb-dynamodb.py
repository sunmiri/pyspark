#https://spark.apache.org/docs/latest/api/python/index.html

import sys
import random
import pyspark
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from jproperties import Properties
from pyspark.storagelevel import StorageLevel 
from pyspark.sql import Row
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType
from pyspark.sql.functions import col

#https://github.com/audienceproject/spark-dynamodb
class MyPySparkApp:
    def __init__(self, **kwargs):
        print("__init__::kwargs:%s" % kwargs)
        self.appname = kwargs.get("name", kwargs.get("spark.name", "PySpark-Redshift-Redshift"))
        self.conf = SparkConf().setAppName(self.appname).setMaster(kwargs.get("master", kwargs.get("spark.master", "local")))
        print("__init__::self.conf:%s" % self.conf)
        self.sc = SparkContext(conf=self.conf)
        print("__init__::self.sc:%s" % self.sc)
        self.spark = SparkSession.builder.appName(self.appname).getOrCreate()
        print("__init__::self.spark:%s" % self.spark)
        self.spark.sparkContext.setLogLevel('WARN')
        #Local spark env (choices: local, cluster,..)

        self.src_dyd_table=kwargs.get("source.dynamodb_table")
        self.src_file=kwargs.get("source.file")
        self.sink_dyd_table=kwargs.get("sink.dynamodb_table")
        
        
    def start(self):
        print("start")
        self.dydSrcDF = self.spark.read.format("dynamodb") \
            .option("tableName", self.src_dyd_table) \
            .load()
        print("readData::dydSrcDF::", self.dydSrcDF)
        self.dydSrcDF.show()

        fileSrcDF = self.spark.read.format('csv').options(header='true').options(inferSchema='true').load(self.src_file).cache()
        print("readData::fileSrcDF::", fileSrcDF)
        fileSrcDF.show()
        
        fileSrcDF.write.option("tableName", self.sink_dyd_table).mode("append").format("dynamodb").save()

        self.sc.stop()
        
        

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
    psl = MyPySparkApp(**kw)
    psl.start()

"""
#testtable: 	dept_name, message, number
#emp:		id, name, number, description
#dept:		id, name, description
select * from dept;

create table emp (emp_number int, emp_name varchar, emp_id int, description varchar);
insert into emp values (1001, 'Sunil', 1, 'Sunil');
insert into emp values (1002, 'Sandeep', 2, 'Sandeep');
insert into emp values (1003, 'Dinesh', 3, 'Dinesh');
insert into emp values (1004, 'Praveen', 4, 'Praveen');
insert into emp values (1005, 'Amar', 5, 'Amar');
select * from emp;

create table projects (proj_id int, proj_name varchar, proj_desc varchar);
insert into projects values (1001, 'Proj1', 'Proj1');
insert into projects values (1002, 'Proj2', 'Proj2');
insert into projects values (1003, 'Proj3', 'Proj3');
insert into projects values (1004, 'Proj4', 'Proj4');
insert into projects values (1005, 'Proj5', 'Proj5');
select * from projects;

create table emp_dept (emp_number int, emp_name varchar, dept_name varchar, emp_id int, dept_id int);

create table emp_proj (emp_number int, emp_name varchar, proj_name varchar, emp_id int, proj_id int);

create table emp_details (emp_number int, emp_name varchar, emp_id int, projects_count int, projects_names varchar, dept_count int, dept_name varchar);

"""