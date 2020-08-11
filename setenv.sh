export APP_HOME_DIR=/mnt/c/Training/PySpark/pyspark
#$(dirname "$0")/../
cd $APP_HOME_DIR
APP_HOME_DIR=$(pwd)

export SPARK_HOME=$APP_HOME_DIR/lib/spark-3.0.0-bin-hadoop3.2
export PATH=$PATH:$APP_HOME_DIR/lib/spark-3.0.0-bin-hadoop3.2/bin
export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.4-src.zip:$PYTHONPATH
export PATH=$SPARK_HOME/python:$PATH
echo "SPARK_HOME $SPARK_HOME"
echo "PATH $PATH"

mkdir -p $APP_HOME_DIR/venv/
python3 -m venv $APP_HOME_DIR/venv
source $APP_HOME_DIR/venv/bin/activate
python --version
pip --version
pip install pyspark jproperties