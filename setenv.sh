export MYDIR=/Users/sunilmiriyala/CirrusSS/A-Cloud/Training/PySpark
export SPARK_HOME=$MYDIR/spark-3.0.0-bin-hadoop3.2
export PATH=$PATH:$MYDIR/spark-3.0.0-bin-hadoop3.2/bin
export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.4-src.zip:$PYTHONPATH
export PATH=$SPARK_HOME/python:$PATH
echo "SPARK_HOME $SPARK_HOME"
echo "PATH $PATH"
