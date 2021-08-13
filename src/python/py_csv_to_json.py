# Databricks notebook source
print(spark)
filePath = "/FileStore/tables/customers.csv"
read = spark.read.format('csv').options(header='true').options(inferSchema='true').load(filePath)
print(read)
read.show()
read.write.format("json").mode("overwrite").save("/FileStore/tables/customers.json")

# COMMAND ----------

# MAGIC %fs ls /FileStore/tables/customers.json

# COMMAND ----------

dbutils.fs.head("dbfs:/FileStore/tables/customers.json/part-00000-tid-6685263526448070280-7b37ea46-0a40-43cc-8bde-2ac6660b59d3-2-1-c000.json")

# COMMAND ----------

dbutils.fs.rm("/FileStore/tables/applications.json")

# COMMAND ----------

filePath = "/FileStore/tables/applications.json"
read = spark.read.format('json').option("multiline","true").load(filePath)
print(read)
read.show()

print(type(read))

def printDetails(row):
  print("printDetails:", row)
  
read.foreach(printDetails)
