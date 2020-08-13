#Install AWS Cli
#https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html

################ One Time ################
#####1
#Create and download KeyPair
#AWS-EC2-KeyPair
#Download
#cp ~/Downloads/<keypair>.pem ~/.ssh/

#####2
#aws configure aws_access_key_id=<IAM-User-SecurityCreds-AccesskeyID> aws_secret_access_key=<IAM-User-SecurityCreds-SecretAccessKey>
    #Region=us-east-1
    #output:json

#####3
#S3 Bucket Setup
#Create Bucket
aws s3 mb s3://pyspark-sunil/ --region us-east-1
#Copy Bootstrap
aws s3 cp aws_bootstrap.sh s3://pyspark-sunil/
#Copy Data Files
aws s3 cp --recursive data s3://pyspark-sunil/data
#Copy Code, Props and Configs
aws s3 cp --recursive src/python s3://pyspark-sunil/run/
aws s3 cp scripts/pyspark-csv.properties s3://pyspark-sunil/run/
aws s3 cp scripts/pyspark-kinesis.properties s3://pyspark-sunil/run/
aws s3 cp scripts/spark_config.json s3://pyspark-sunil/run/
#Copy Libs
aws s3 cp lib/spark-streaming-kinesis-asl-assembly_2.12-3.0.0.jar s3://pyspark-sunil/lib/
aws s3 cp lib/spark-avro_2.12-3.0.0.jar s3://pyspark-sunil/lib/