export APP_HOME_DIR=/Users/sunilmiriyala/CirrusSS/A-Cloud/Training/pyspark

# Launch
aws emr create-cluster --name "SparkStep-RunKinesis" \
    --release-label emr-6.0.0 \
    --applications Name=Spark \
    --log-uri s3://pyspark-sunil/logs/ \
    --ec2-attributes KeyName=sunil-aws-emr-key-pair-east1 \
    --instance-type m4.large \
    --instance-count 2 \
    --bootstrap-actions Path=s3://pyspark-sunil/aws_bootstrap.sh \
    --steps Type=Spark,Name="Spark-Job-RunKinesis",ActionOnFailure=CONTINUE,Args=[--deploy-mode,client,--master,yarn,--jars,s3://pyspark-sunil/lib/spark-streaming-kinesis-asl-assembly_2.12-3.0.0.jar,s3://pyspark-sunil/run/pyspark-kinesis.py,--p,/tmp/pyspark-kinesis.properties] \
    --use-default-roles \
    --auto-terminate

# Check Status
aws emr list-clusters --active

# Login
# aws emr ssh --cluster-id j-3SD91U2E1L2QX --key-pair-file ~/.ssh/mykey.pem