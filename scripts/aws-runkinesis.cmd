set APP_HOME_DIR=%APP_HOME_DIR%

aws s3 cp %APP_HOME_DIR%\src\python\pyspark-kinesis.py s3://%AWS_BUCKET_NAME%/run/
aws s3 cp %APP_HOME_DIR%\scripts\pyspark-kinesis.properties s3://%AWS_BUCKET_NAME%/run/

rem Launch
aws emr create-cluster --name "SparkStep-RunKinesis" ^
    --release-label emr-6.0.0 ^
    --applications Name=Spark ^
    --log-uri s3://%AWS_BUCKET_NAME%/logs/ ^
    --ec2-attributes KeyName=sunil-aws-emr-key-pair-east1 ^
    --instance-type m4.large ^
    --instance-count 2 ^
    --bootstrap-actions Path=s3://%AWS_BUCKET_NAME%/aws_bootstrap.sh ^
    --steps Type=Spark,Name="Spark-Job-RunKinesis",ActionOnFailure=CONTINUE,Args=[--deploy-mode,client,--master,yarn,--num-executors,2,--executor-cores,2,--jars,s3://%AWS_BUCKET_NAME%/lib/spark-streaming-kinesis-asl-assembly_2.12-3.0.0.jar,s3://%AWS_BUCKET_NAME%/run/pyspark-kinesis.py,--p,/tmp/pyspark-kinesis.properties] ^
    --use-default-roles ^
    --auto-terminate

rem Check Status
aws emr list-clusters --active

rem Login
rem aws emr ssh --cluster-id j-3SD91U2E1L2QX --key-pair-file ~/.ssh/mykey.pem