#!/usr/bin/bash
export APP_HOME_DIR=/Users/sunilmiriyala/CirrusSS/A-Cloud/Training/pyspark

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

#Runtime: it picks from <home>/.aws/credentials (aws configure)
#export AWS_ACCESS_KEY_ID=AKIA6AACCFDFGQHBQMNG
#export AWS_SECRET_ACCESS_KEY=
export SPARK_HOME=$APP_HOME_DIR/lib/spark-3.0.0-bin-hadoop3.2
export PATH=$PATH:$APP_HOME_DIR/lib/spark-3.0.0-bin-hadoop3.2/bin
export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9-src.zip:$PYTHONPATH
export PATH=$SPARK_HOME/python:$PATH
echo "SPARK_HOME $SPARK_HOME"
echo "PYTHONPATH: $PYTHONPATH"
echo "PATH $PATH"

cd $APP_HOME_DIR/src/python/
#Option:1
$SPARK_HOME/bin/spark-submit --master local[4] \
    --jars "$APP_HOME_DIR/lib/*.jar" \
    pyspark-kinesis.py --p $APP_HOME_DIR/scripts/pyspark-kinesis.properties
    #$APP_HOME_DIR/scripts/pyspark-kinesis.properties

#Option:2
#pyspark pyspark-csv.py $APP_HOME_DIR/src/python/pyspark-csv.properties