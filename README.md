GIT

1: CLONE (one time)

git clone https://github.com/sunmiri/pyspark.git

2: Get Latest:

cd <your dir>

git pull

3: Check-In & Commit

git status

Will list changes

>>for-each change:

git add <file-with-patch>

>>Once ready to push/commit

git commit -m "some verbose comment"

git remote set-url origin https://sunmiri@github.com/sunmiri/pyspark.git

git push

===========


Api: https://spark.apache.org/docs/latest/api/python/index.html

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
