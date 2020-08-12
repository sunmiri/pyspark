#!/usr/bin/bash
APP_HOME_DIR=/Users/sunilmiriyala/CirrusSS/A-Cloud/Training/pyspark
echo "APP_HOME_DIR $APP_HOME_DIR"

export SPARK_HOME=$APP_HOME_DIR/lib/spark-3.0.0-bin-hadoop3.2
export PATH=$PATH:$APP_HOME_DIR/lib/spark-3.0.0-bin-hadoop3.2/bin
export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9-src.zip:$PYTHONPATH
export PATH=$SPARK_HOME/python:$PATH
echo "SPARK_HOME $SPARK_HOME"
echo "PYTHONPATH: $PYTHONPATH"
echo "PATH $PATH"

cd $APP_HOME_DIR
if [[ -d "$APP_HOME_DIR/venv" ]]
then
    echo "Sourcing Python Virtual Env"
    source $APP_HOME_DIR/venv/bin/activate
else
    echo "Creating Virtual Env in current dir $(pwd)"
    python3 -m venv venv
    source $APP_HOME_DIR/venv/bin/activate
fi
python --version
pip --version
pip install pyspark jproperties argparse json