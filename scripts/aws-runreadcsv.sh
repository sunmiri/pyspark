APP_HOME_DIR=$(dirname "$0")/../
cd $APP_HOME_DIR
APP_HOME_DIR=$(pwd)

#Launch
aws emr create-cluster --name "SparkStep-RunCSV" \
    --release-label emr-6.0.0 \
    --applications Name=Spark \
    --log-uri s3://pyspark-examples/logs/ \
    --ec2-attributes KeyName=sunil-aws-emr-key-pair-east1 \
    --instance-type m4.large \
    --instance-count 3 \
    --bootstrap-actions Path=s3://pyspark-examples/emr_bootstrap.sh \
    --steps Type=Spark,Name="Spark-Job-RunCSV",ActionOnFailure=CONTINUE,Args=[--deploy-mode,cluster,--master,yarn,s3://pyspark-examples/pyspark-csv.py] \
    --use-default-roles \
    --auto-terminate

#Check Status
aws emr list-clusters

#Login
#aws emr ssh --cluster-id j-3SD91U2E1L2QX --key-pair-file ~/.ssh/mykey.pem