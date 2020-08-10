Api:
https://spark.apache.org/docs/latest/api/python/index.html

Run as Py File:
A:
source /opt/codebase/PYTHON3/bin/activate 
cd <your-path>/PySpark/
sh ./setenv.sh
echo $SPARK_HOME
cd src/python/
$SPARK_HOME/bin/spark-submit pyspark-local.py

B:
pip install pyspark
python pyspark-local.py

Run on Terminal:
source /opt/codebase/PYTHON3/bin/activate
pip install pyspark
cd <your-path>/PySpark
sh ./setenv.sh
cd <your-path>/PySpark/spark-3.0.0-bin-hadoop3.2/bin
./pyspark --master local[2]
...
...
Using Python version 3.7.3 (v3.7.3:ef4ec6ed12, Mar 25 2019 16:52:21)
SparkSession available as 'spark'.