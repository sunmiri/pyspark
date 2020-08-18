export APP_HOME_DIR=/Users/sunilmiriyala/CirrusSS/A-Cloud/Training/pyspark
export AWS_BUCKET_NAME=pyspark-sunil
export KEY_PAIR_NAME=sunil-aws-emr-key-pair-east1
#upload latest bootstrap and hdp-configs
aws s3 cp $APP_HOME_DIR/aws_bootstrap.sh s3://$AWS_BUCKET_NAME/
aws s3 cp $APP_HOME_DIR/aws_hdp_config.json s3://$AWS_BUCKET_NAME/
#upload latest prop and file
aws s3 cp --recursive $APP_HOME_DIR/data s3://$AWS_BUCKET_NAME/data
aws s3 cp $APP_HOME_DIR/src/python/pyspark-csv.py s3://$AWS_BUCKET_NAME/run/
aws s3 cp $APP_HOME_DIR/scripts/pyspark-csv.properties s3://$AWS_BUCKET_NAME/run/
#Upload needed jars in the s3
aws s3 cp $APP_HOME_DIR/lib/RedshiftJDBC42-no-awssdk-1.2.45.1069.jar s3://$AWS_BUCKET_NAME/lib/
aws s3 cp $APP_HOME_DIR/lib/spark-streaming-kinesis-asl-assembly_2.12-3.0.0.jar s3://$AWS_BUCKET_NAME/lib/
aws s3 cp $APP_HOME_DIR/lib/spark-avro_2.12-3.0.0.jar s3://$AWS_BUCKET_NAME/lib/
#Launch
aws emr create-cluster --name "SparkStep-RunCSV" \
    --release-label emr-6.0.0 \
    --applications Name=Spark \
    --log-uri s3://$AWS_BUCKET_NAME/logs/ \
    --ec2-attributes KeyName=$KEY_PAIR_NAME \
    --instance-type m4.large \
    --instance-count 2 \
    --bootstrap-actions Path=s3://$AWS_BUCKET_NAME/aws_bootstrap.sh \
    --steps Type=Spark,Name="Spark-Job-RunCSV",ActionOnFailure=CONTINUE,Args=[--deploy-mode,cluster,--master,yarn,--jars,/tmp/*.jar,s3://$AWS_BUCKET_NAME/run/pyspark-csv.py,--p,/tmp/pyspark-csv.properties] \
    --configurations file://../aws_hdp_config.json \
    --use-default-roles \
    --auto-terminate

#Check Status
aws emr list-clusters --active

#Login
#aws emr ssh --cluster-id j-3SD91U2E1L2QX --key-pair-file ~/.ssh/mykey.pem