APP_HOME_DIR=$(dirname "$0")/../
cd $APP_HOME_DIR
APP_HOME_DIR=$(pwd)

source /opt/codebase/PYTHON3/bin/activate

cd $APP_HOME_DIR
#sh $APP_HOME_DIR/setenv.sh
export SPARK_HOME=$APP_HOME_DIR/lib/spark-3.0.0-bin-hadoop3.2
export PATH=$PATH:$APP_HOME_DIR/lib/spark-3.0.0-bin-hadoop3.2/bin
export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.4-src.zip:$PYTHONPATH
export PATH=$SPARK_HOME/python:$PATH
echo "SPARK_HOME $SPARK_HOME"
echo "PATH $PATH"

cd $APP_HOME_DIR/src/python/
#Option:1
$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-avro_2.12:3.0.0 pyspark-csv.py $APP_HOME_DIR/src/python/pyspark-csv.properties

#Option:2
#pyspark pyspark-csv.py $APP_HOME_DIR/src/python/pyspark-csv.properties