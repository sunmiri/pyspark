#!/bin/bash -xe
export AWS_BUCKET_NAME=pyspark-sunil
export SPARK_HOME=/usr/lib/spark
export PYSPARK_PYTHON=/usr/bin/python3

python3 --version

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
pip3 install pyspark jproperties findspark

#aws s3 cp s3://$AWS_BUCKET_NAME/run/pyspark-kinesis.properties /tmp/
#aws s3 cp s3://$AWS_BUCKET_NAME/run/pyspark-csv.properties /tmp/
aws s3 cp s3://$AWS_BUCKET_NAME/run/pyspark-kafka.properties /tmp/

#Hack. Let these jars be in /tmp on each worker/master/driver node
#aws s3 cp s3://$AWS_BUCKET_NAME/lib/RedshiftJDBC42-no-awssdk-1.2.45.1069.jar /tmp/
#aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-streaming-kinesis-asl_2.12-3.0.0.jar /tmp/
#aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-streaming-kinesis-asl-assembly_2.12-3.0.0.jar /tmp/
#aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-sql-kinesis_2.11-1.1.4_spark-2.4.jar /tmp/
aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-avro_2.12-3.0.0.jar /tmp/
aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-sql_2.12-3.0.0.jar /tmp/
aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-catalyst_2.12-3.0.0.jar /tmp/
aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-sql-kafka-0-10_2.12-3.0.0.jar /tmp/
aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-streaming-kafka-0-10-assembly_2.12-3.0.0.jar /tmp/
aws s3 cp s3://$AWS_BUCKET_NAME/lib/commons-pool2-2.8.1.jar /tmp/

#Making Application Dependencies available in workers
if [[ -d "$SPARK_HOME" ]]
then
    #aws s3 cp s3://$AWS_BUCKET_NAME/lib/RedshiftJDBC42-no-awssdk-1.2.45.1069.jar $SPARK_HOME/jars/
    #aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-streaming-kinesis-asl_2.12-3.0.0.jar /jars/
    #aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-streaming-kinesis-asl-assembly_2.12-3.0.0.jar $SPARK_HOME/jars/
    #aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-sql-kinesis_2.11-1.1.4_spark-2.4.jar $SPARK_HOME/jars/
    aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-avro_2.12-3.0.0.jar $SPARK_HOME/jars/
    aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-sql_2.12-3.0.0.jar $SPARK_HOME/jars/
    aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-catalyst_2.12-3.0.0.jar $SPARK_HOME/jars/
    aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-sql-kafka-0-10_2.12-3.0.0.jar $SPARK_HOME/jars/
    aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-streaming-kafka-0-10-assembly_2.12-3.0.0.jar $SPARK_HOME/jars/
    aws s3 cp s3://$AWS_BUCKET_NAME/lib/commons-pool2-2.8.1.jar $SPARK_HOME/jars/
    echo "Copied Jar to SPARK_HOME"
else
    echo "$SPARK_HOME is Not Available Yet. Will use /tmp"
    #aws s3 cp s3://$AWS_BUCKET_NAME/lib/RedshiftJDBC42-no-awssdk-1.2.45.1069.jar /tmp/
    #aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-streaming-kinesis-asl_2.12-3.0.0.jar /tmp/
    #aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-streaming-kinesis-asl-assembly_2.12-3.0.0.jar /tmp/
    #aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-sql-kinesis_2.11-1.1.4_spark-2.4.jar /tmp/
    aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-avro_2.12-3.0.0.jar /tmp/
    aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-sql_2.12-3.0.0.jar /tmp/
    aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-catalyst_2.12-3.0.0.jar /tmp/
    aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-sql-kafka-0-10_2.12-3.0.0.jar /tmp/
    aws s3 cp s3://$AWS_BUCKET_NAME/lib/spark-streaming-kafka-0-10-assembly_2.12-3.0.0.jar /tmp/
    aws s3 cp s3://$AWS_BUCKET_NAME/lib/commons-pool2-2.8.1.jar /tmp/
    echo "Copied Jar to TMP"
fi