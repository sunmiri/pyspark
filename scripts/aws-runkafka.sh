export APP_HOME_DIR=/Users/sunilmiriyala/CirrusSS/A-Cloud/Training/pyspark
export AWS_BUCKET_NAME=pyspark-sunil
export KEY_PAIR_NAME=sunil-aws-emr-key-pair-east1
export MASTER_SLAVE_SECURITY_GROUP=sg-073ee2fad4a22aee5
export SUBNET=subnet-0c6eca5d53763c26d
#upload latest bootstrap and hdp-configs
aws s3 cp $APP_HOME_DIR/aws_bootstrap.sh s3://$AWS_BUCKET_NAME/
aws s3 cp $APP_HOME_DIR/aws_hdp_config.json s3://$AWS_BUCKET_NAME/
#Upload needed jars in the s3
aws s3 cp $APP_HOME_DIR/lib/spark-avro_2.12-3.0.0.jar s3://$AWS_BUCKET_NAME/lib/
aws s3 cp $APP_HOME_DIR/lib/spark-sql_2.12-3.0.0.jar s3://$AWS_BUCKET_NAME/lib/
aws s3 cp $APP_HOME_DIR/lib/spark-catalyst_2.12-3.0.0.jar s3://$AWS_BUCKET_NAME/lib/
aws s3 cp $APP_HOME_DIR/lib/spark-sql-kafka-0-10_2.12-3.0.0.jar s3://$AWS_BUCKET_NAME/lib/
aws s3 cp $APP_HOME_DIR/lib/spark-streaming-kafka-0-10-assembly_2.12-3.0.0.jar s3://$AWS_BUCKET_NAME/lib/
aws s3 cp $APP_HOME_DIR/lib/commons-pool2-2.8.1.jar s3://$AWS_BUCKET_NAME/lib/

#upload latest prop and file
aws s3 cp $APP_HOME_DIR/scripts/pyspark-kafka.properties s3://$AWS_BUCKET_NAME/run/
aws s3 cp $APP_HOME_DIR/src/python/pyspark-kafka.py s3://$AWS_BUCKET_NAME/run/

# Launch
aws emr create-cluster --name "SparkStep-Runkafka" \
    --release-label emr-6.0.0 \
    --applications Name=Spark \
    --log-uri s3://$AWS_BUCKET_NAME/logs/ \
    --ec2-attributes KeyName=$KEY_PAIR_NAME,SubnetId=$SUBNET,EmrManagedMasterSecurityGroup=$MASTER_SLAVE_SECURITY_GROUP,EmrManagedSlaveSecurityGroup=$MASTER_SLAVE_SECURITY_GROUP \
    --instance-type m4.large \
    --instance-count 2 \
    --bootstrap-actions Path=s3://$AWS_BUCKET_NAME/aws_bootstrap.sh \
    --steps Type=Spark,Name="Spark-Job-Runkafka",ActionOnFailure=CONTINUE,Args=[--deploy-mode,client,--master,yarn,--num-executors,2,--executor-cores,2,--jars,/tmp/*.jar,s3://$AWS_BUCKET_NAME/run/pyspark-kafka.py,--p,/tmp/pyspark-kafka.properties] \
    --configurations file://../aws_hdp_config.json \
    --use-default-roles \
    --auto-terminate

# Check Status
aws emr list-clusters --active

# Login
# aws emr ssh --cluster-id j-3SD91U2E1L2QX --key-pair-file ~/.ssh/mykey.pem