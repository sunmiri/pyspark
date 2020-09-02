set APP_HOME_DIR=%APP_HOME_DIR%
set AWS_BUCKET_NAME=%AWS_BUCKET_NAME%
set KEY_PAIR_NAME=%KEY_PAIR_NAME%
set MASTER_SLAVE_SECURITY_GROUP=sg-073ee2fad4a22aee5
set SUBNET=subnet-0c6eca5d53763c26d
rem upload latest bootstrap and hdp-configs
aws s3 cp %APP_HOME_DIR%\aws_bootstrap.sh s3://%AWS_BUCKET_NAME%/
aws s3 cp %APP_HOME_DIR%\aws_hdp_config.json s3://%AWS_BUCKET_NAME%/
rem Upload needed jars in the s3
aws s3 cp %APP_HOME_DIR%\lib\spark-avro_2.12-3.0.0.jar s3://%AWS_BUCKET_NAME%/lib/
aws s3 cp %APP_HOME_DIR%\lib\spark-sql_2.12-3.0.0.jar s3://%AWS_BUCKET_NAME%/lib/
aws s3 cp %APP_HOME_DIR%\lib\spark-catalyst_2.12-3.0.0.jar s3://%AWS_BUCKET_NAME%/lib/
aws s3 cp %APP_HOME_DIR%\lib\spark-sql-kafka-0-10_2.12-3.0.0.jar s3://%AWS_BUCKET_NAME%/lib/
aws s3 cp %APP_HOME_DIR%\lib\spark-streaming-kafka-0-10-assembly_2.12-3.0.0.jar s3://%AWS_BUCKET_NAME%/lib/
aws s3 cp %APP_HOME_DIR%\lib\commons-pool2-2.8.1.jar s3://%AWS_BUCKET_NAME%/lib/
rem upload latest prop and file
aws s3 cp %APP_HOME_DIR%\src\python\pyspark-kafka.py s3://%AWS_BUCKET_NAME%/run/
aws s3 cp %APP_HOME_DIR%\scripts\pyspark-kafka.properties s3://%AWS_BUCKET_NAME%/run/
rem  Launch
aws emr create-cluster --name "SparkStep-Runkafka" ^
    --release-label emr-6.0.0 ^
    --applications Name=Spark ^
    --log-uri s3://%AWS_BUCKET_NAME%/logs/ ^
    --ec2-attributes KeyName=%KEY_PAIR_NAME% ^
    --instance-type m4.large ^
    --instance-count 2 ^
    --bootstrap-actions Path=s3://%AWS_BUCKET_NAME%/aws_bootstrap.sh ^
    --steps Type=Spark,Name="Spark-Job-Runkafka",ActionOnFailure=CONTINUE,Args=[--deploy-mode,client,--master,yarn,--num-executors,2,--executor-cores,2,--jars,/tmp/*.jar,s3://%AWS_BUCKET_NAME%/run/pyspark-kafka.py,--p,/tmp/pyspark-kafka.properties] ^
    --configurations file://..\aws_hdp_config.json ^
    --use-default-roles ^
    --auto-terminate

rem  Check Status
aws emr list-clusters --active
