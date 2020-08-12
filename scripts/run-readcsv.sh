#!/usr/bin/bash
APP_HOME_DIR=/Users/sunilmiriyala/CirrusSS/A-Cloud/Training/pyspark

cd $APP_HOME_DIR
if [[ -d "$APP_HOME_DIR/venv" ]]
then
    echo "Sourcing Python Virtual Env"
    source $APP_HOME_DIR/venv/bin/activate
    pip install pyspark jproperties argparse json
else
    echo "Creating Virtual Env in current dir $(pwd)"
    python3 -m venv venv
    source $APP_HOME_DIR/venv/bin/activate
    pip install pyspark jproperties argparse json
fi

export SPARK_HOME=$APP_HOME_DIR/lib/spark-3.0.0-bin-hadoop3.2
export PATH=$PATH:$APP_HOME_DIR/lib/spark-3.0.0-bin-hadoop3.2/bin
export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9-src.zip:$PYTHONPATH
export PATH=$SPARK_HOME/python:$PATH
echo "SPARK_HOME $SPARK_HOME"
echo "PYTHONPATH: $PYTHONPATH"
echo "PATH $PATH"

cd $APP_HOME_DIR/src/python/
#Option:1
$SPARK_HOME/bin/spark-submit \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0-preview2,org.apache.spark:spark-avro_2.12:3.0.0 \
    pyspark-csv.py --p $APP_HOME_DIR/scripts/pyspark-csv.properties

#Option:2
#pyspark pyspark-csv.py $APP_HOME_DIR/src/python/pyspark-csv.properties