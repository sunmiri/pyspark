print(spark)
filePath = "/FileStore/tables/customers.csv"
spark.read.format('csv').options(header='true').options(inferSchema='true').load(filePath).write.format("json").mode("overwrite").save("/FileStore/tables/customers.json")
