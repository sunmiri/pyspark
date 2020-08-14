rem #Install AWS Cli
rem #https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html

rem ################ One Time ################
rem #####1
rem #Create and download KeyPair
rem #AWS-EC2-KeyPair
rem #Download
rem #cp ~/Downloads/<keypair>.pem ~/.ssh/

rem #####2
rem #aws configure aws_access_key_id=<IAM-User-SecurityCreds-AccesskeyID> aws_secret_access_key=<IAM-User-SecurityCreds-SecretAccessKey>
    rem #Region=us-east-1
    rem #output:json

rem #####3
rem #S3 Bucket Setup
rem #Create Bucket
aws s3 mb s3://%AWS_BUCKET_NAME%/ --region us-east-1
rem #Copy Bootstrap
aws s3 cp aws_bootstrap.sh s3://%AWS_BUCKET_NAME%/
rem #Copy Data Files
aws s3 cp --recursive data s3://%AWS_BUCKET_NAME%/data
rem #Copy Code, Props and Configs
aws s3 cp --recursive src/python s3://%AWS_BUCKET_NAME%/run/
aws s3 cp scripts/pyspark-csv.properties s3://%AWS_BUCKET_NAME%/run/
aws s3 cp scripts/pyspark-kinesis.properties s3://%AWS_BUCKET_NAME%/run/
aws s3 cp scripts/spark_config.json s3://%AWS_BUCKET_NAME%/run/
rem #Copy Libs
aws s3 cp lib/spark-streaming-kinesis-asl-assembly_2.12-3.0.0.jar s3://%AWS_BUCKET_NAME%/lib/
aws s3 cp lib/spark-avro_2.12-3.0.0.jar s3://%AWS_BUCKET_NAME%/lib/