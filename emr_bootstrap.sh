#!/bin/bash -xe

#sudo yum install -y python37 python37-pip

python --version
#python -m pip install pyspark jproperties

python3 --version
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
pip3 install boto3 pyspark jproperties

export SPARK_HOME=/usr/lib/spark
export PYSPARK_PYTHON=/usr/bin/python3

#https://aws.amazon.com/premiumsupport/knowledge-center/emr-pyspark-python-3x/
#sudo sed -i -e '$a\export PYSPARK_PYTHON=/usr/bin/python3' /etc/spark/conf/spark-env.sh
