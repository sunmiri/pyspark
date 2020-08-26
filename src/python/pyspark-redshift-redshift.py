#https://spark.apache.org/docs/latest/api/python/index.html

import sys
import random
import pyspark
from pyspark.streaming.kinesis import KinesisUtils, InitialPositionInStream
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

        self.src_rsf_user=kwargs.get("source.redshift_user","awsuser")
        self.src_rsf_pswd=kwargs.get("source.redshift_pass",None)
        self.src_rsf_port=kwargs.get("source.redshift_port",5439)
        self.src_rsf_db=kwargs.get("source.redshift_db","dev")
        self.src_rsf_table=kwargs.get("source.redshift_table","dept,emp,projects")
        self.src_rsf_jdbc_url=kwargs.get("source.redshift_jdbc_url",None)

        self.snk_rsf_user=kwargs.get("sink.redshift_user","awsuser")
        self.snk_rsf_pswd=kwargs.get("sink.redshift_pass",None)
        self.snk_rsf_port=kwargs.get("sink.redshift_port",5439)
        self.snk_rsf_db=kwargs.get("sink.redshift_db","dev")
        self.snk_rsf_table=kwargs.get("sink.redshift_table","emp_dept,emp_proj,emp_details")
        self.snk_rsf_jdbc_url=kwargs.get("sink.redshift_jdbc_url",None)

    def start(self):
        print("start")
        src_tables = self.src_rsf_table.split(",")
        print("start::src_tables:%s" % src_tables)
        self.deptDF = self.spark.read.format("jdbc") \
            .option("url", self.src_rsf_jdbc_url) \
            .option("dbtable", src_tables[0]) \
            .option("user", self.src_rsf_user) \
            .option("password", self.src_rsf_pswd) \
            .option("driver", "com.amazon.redshift.jdbc42.Driver") \
            .load()
        print("readData::deptDF::", self.deptDF)
        self.deptDF.show()
        self.deptDF.describe()

        self.empDF = self.spark.read.format("jdbc") \
            .option("url", self.src_rsf_jdbc_url) \
            .option("dbtable", src_tables[1]) \
            .option("user", self.src_rsf_user) \
            .option("password", self.src_rsf_pswd) \
            .option("driver", "com.amazon.redshift.jdbc42.Driver") \
            .load()
        print("readData::empDF::", self.empDF)
        self.empDF.show()
        self.empDF.describe()

        self.projectsDF = self.spark.read.format("jdbc") \
            .option("url", self.src_rsf_jdbc_url) \
            .option("dbtable", src_tables[2]) \
            .option("user", self.src_rsf_user) \
            .option("password", self.src_rsf_pswd) \
            .option("driver", "com.amazon.redshift.jdbc42.Driver") \
            .load()
        print("readData::projectsDF::", self.projectsDF)
        self.projectsDF.show()
        self.projectsDF.describe()
        
        #emp_number int, emp_name varchar, dept_name varchar, emp_id int, dept_id int
        emp_dept_sch = StructType([StructField('emp_number', IntegerType(), True), StructField('emp_name', StringType(), True), StructField('dept_name', StringType(), True), StructField('emp_id', IntegerType(), True), StructField('dept_id', IntegerType(), True)])
        emp_dept_df = self.spark.createDataFrame(self.spark.sparkContext.emptyRDD(), emp_dept_sch)
        emp_dept_df.printSchema()
        print("emp_dept_df::%s" % type(emp_dept_df))
        
        #emp_number int, emp_name varchar, proj_name varchar, emp_id int, proj_id int
        emp_proj_sch = StructType([StructField('emp_number', IntegerType(), True), StructField('emp_name', StringType(), True), StructField('proj_name', StringType(), True), StructField('emp_id', IntegerType(), True), StructField('proj_id', IntegerType(), True)])
        emp_proj_df = self.spark.createDataFrame(self.spark.sparkContext.emptyRDD(), emp_proj_sch)
        emp_proj_df.printSchema()
        print("emp_proj_df::%s" % type(emp_proj_df))
        
        #Adding Empt to couple of depts
        #print("Sample DeptDF Rows:")
        #self.deptDF.sample(0.5).show()

        userinput_dept = ["Dept1", "Dept2"]
        userinput_emp = "Sunil"
        userinput_proj = ["Proj1", "Proj4"]
        """
        for erow in self.empDF.rdd.collect():
            if erow['emp_name'] == userinput_emp:
                for drow in self.deptDF.rdd.collect():
                    print("erow:", erow, ",drow:", drow)
                    if drow['name'] in userinput_dept:
                        #emp_number int, emp_name varchar, dept_name varchar, emp_id int, dept_id int
                        newDf = self.spark.createDataFrame([(erow['emp_number'], erow['emp_name'], drow['name'], erow['emp_id'], drow['id'])], emp_dept_sch)
                        emp_dept_df = emp_dept_df.union(newDf)
        emp_dept_df.show()
        """
        self.empDF.createOrReplaceTempView("emp")
        self.deptDF.createOrReplaceTempView("dept")
        sql = "select e.emp_number, e.emp_name, d.name as dept_name, emp_id, d.id as dept_id from emp e, dept d where e.emp_name in (\"Sandeep\") and d.name in (\"Dept3\",\"Dept1\")"
        print("sql:%s" % sql)
        emp_dept_df = self.spark.sql(sql)
        emp_dept_df.show()
        emp_dept_df.write.mode("append") \
            .format("jdbc") \
            .option("url", self.snk_rsf_jdbc_url) \
            .option("dbtable", "emp_dept") \
            .option("user", self.snk_rsf_user) \
            .option("password", self.snk_rsf_pswd) \
            .option("driver", "com.amazon.redshift.jdbc42.Driver") \
            .save()
        print("processRDD::successfully wrote the emp_dept_df")
        
        """
        for erow in self.empDF.rdd.collect():
            if erow['emp_name'] == userinput_emp:
                for prow in self.projectsDF.rdd.collect():
                    print("erow:", erow, ",prow:", prow)
                    if prow['proj_name'] in userinput_proj:
                        #proj_id int, proj_name varchar
                        #emp_number int, emp_name varchar, proj_name varchar, emp_id int, proj_id int
                        newDf = self.spark.createDataFrame([(erow['emp_number'], erow['emp_name'], prow['proj_name'], erow['emp_id'], prow['proj_id'])], emp_proj_sch)
                        emp_proj_df = emp_proj_df.union(newDf)
        emp_proj_df.show()
        """
        self.empDF.createOrReplaceTempView("emp")
        self.projectsDF.createOrReplaceTempView("projects")
        #emp_number int, emp_name varchar, proj_name varchar, emp_id int, proj_id int
        sql = "select e.emp_number, e.emp_name, p.proj_name, e.emp_id, p.proj_id from emp e, projects p where e.emp_name in (\"Sandeep\") and p.proj_name in (\"Proj5\",\"Proj2\")"
        print("sql:%s" % sql)
        emp_proj_df = self.spark.sql(sql)
        emp_proj_df.show()
        emp_proj_df.write.mode("append") \
            .format("jdbc") \
            .option("url", self.snk_rsf_jdbc_url) \
            .option("dbtable", "emp_proj") \
            .option("user", self.snk_rsf_user) \
            .option("password", self.snk_rsf_pswd) \
            .option("driver", "com.amazon.redshift.jdbc42.Driver") \
            .save()
        print("processRDD::successfully wrote the emp_proj_df")
        
        emp_proj_df.createOrReplaceTempView("emp_proj")
        emp_dept_df.createOrReplaceTempView("emp_dept")

        #emp_number int, emp_name varchar, emp_id int, projects_count int, projects_names varchar, dept_count int, dept_name varchar
        emp_details = "select ed.emp_number, ed.emp_name, count(distinct(ed.dept_id)) as dept_count, CAST(collect_set(distinct(ed.dept_name)) AS STRING) as dept_name, count(distinct(ep.proj_id)) as projects_count, CAST(collect_set(distinct(ep.proj_name)) AS STRING) as projects_names from emp_dept ed inner join emp_proj ep on ed.emp_id = ep.emp_id group by ed.emp_number, ed.emp_name "
        emp_details_df = self.spark.sql(emp_details)
        emp_details_df.show()

        #for ee in self.empDF:
            #for ed in self.deptDF.sample(0.5):
                #newDf = self.sc.parallelize([Row(emp_number=ee.emp_number, emp_name=ee.emp_name, dept_name=ed.dept_name, emp_id=ee.emp_id, dept_id=ed.dept_id)]).toDF()
                #print(ee.emp_number.getItem(0), ee.emp_name.getItem(0), ed.dept_name.getItem(0), ee.emp_id.getItem(0), ed.dept_id.getItem(0))
                #newDf = self.spark.createDataFrame([(ee.emp_number, ee.emp_name, ed.dept_name, ee.emp_id, ed.dept_id)], [int, str, str, int, int])
                #emp_dept_df = emp_dept_df.union(newDf)
        
        #Lets persis this new DF
        emp_details_df.write.mode("append") \
            .format("jdbc") \
            .option("url", self.snk_rsf_jdbc_url) \
            .option("dbtable", "emp_details") \
            .option("user", self.snk_rsf_user) \
            .option("password", self.snk_rsf_pswd) \
            .option("driver", "com.amazon.redshift.jdbc42.Driver") \
            .save()
        print("processRDD::successfully wrote the emp_details_df")

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