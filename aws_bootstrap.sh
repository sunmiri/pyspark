#!/bin/bash -xe
export AWS_BUCKET_NAME=pyspark-sunil

export SPARK_HOME=/usr/lib/spark
export PYSPARK_PYTHON=/usr/bin/python3

python3 --version

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
pip3 install pyspark jproperties

aws s3 cp s3://$AWS_BUCKET_NAME/run/pyspark-kinesis.properties /tmp/
aws s3 cp s3://$AWS_BUCKET_NAME/run/pyspark-csv.properties /tmp/

#Hack. Let these jars be in /tmp on each worker/master/driver node
aws s3 cp s3://$AWS_BUCKET_NAME/lib/RedshiftJDBC42-no-awssdk-1.2.45.1069.jar /tmp/
aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-avro_2.12-3.0.0.jar /tmp/
aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-streaming-kinesis-asl_2.12-3.0.0.jar /tmp/
aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-streaming-kinesis-asl-assembly_2.12-3.0.0.jar /tmp/
aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-sql_2.12-3.0.0.jar /tmp/
aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-catalyst_2.12-3.0.0.jar /tmp/

#Making Application Dependencies available in workers
if [[ -d "$SPARK_HOME" ]]
then
    aws s3 cp s3://$AWS_BUCKET_NAME/lib/RedshiftJDBC42-no-awssdk-1.2.45.1069.jar $SPARK_HOME/jars/
    aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-avro_2.12-3.0.0.jar $SPARK_HOME/jars/
    aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-streaming-kinesis-asl_2.12-3.0.0.jar /jars/
    aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-streaming-kinesis-asl-assembly_2.12-3.0.0.jar $SPARK_HOME/jars/
    aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-sql_2.12-3.0.0.jar $SPARK_HOME/jars/
    aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-catalyst_2.12-3.0.0.jar $SPARK_HOME/jars/
    echo "Copied RedshiftJDBC42 Jar"
else
    echo "$SPARK_HOME is Not Available Yet. Will use /tmp"
    aws s3 cp s3://$AWS_BUCKET_NAME/lib/RedshiftJDBC42-no-awssdk-1.2.45.1069.jar /tmp/
    aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-avro_2.12-3.0.0.jar /tmp/
    aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-streaming-kinesis-asl_2.12-3.0.0.jar /tmp/
    aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-streaming-kinesis-asl-assembly_2.12-3.0.0.jar /tmp/
    aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-sql_2.12-3.0.0.jar /tmp/
    aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-catalyst_2.12-3.0.0.jar /tmp/
fi