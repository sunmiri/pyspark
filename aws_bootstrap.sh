#!/bin/bash -xe

export SPARK_HOME=/usr/lib/spark
export PYSPARK_PYTHON=/usr/bin/python3

python3 --version

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
pip3 install pyspark jproperties

aws s3 cp s3://pyspark-sunil/run/pyspark-kinesis.properties /tmp/
aws s3 cp s3://pyspark-sunil/run/pyspark-csv.properties /tmp/