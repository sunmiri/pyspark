set APP_HOME_DIR=C:\Training\PySpark\pyspark
cd %APP_HOME_DIR%

set JAVA_HOME=C:\Program Files\Java\jdk1.8.0_261

set HADOOP_HOME=%APP_HOME_DIR%\lib\spark-2.4.6-bin-hadoop2.7
set SPARK_HOME=%APP_HOME_DIR%\lib\spark-2.4.6-bin-hadoop2.7
set PATH=%PATH%;%APP_HOME_DIR%\lib\spark-2.4.6-bin-hadoop2.7\bin;%JAVA_HOME%\bin;
rem set PYTHONPATH=C:\Program Files (x86)\Python38-32\
set PYTHONPATH=%SPARK_HOME%\python;%SPARK_HOME%\python\lib\py4j-0.10.7-src.zip;%PYTHONPATH%

rem Launch
aws emr create-cluster --name "SparkStep-RunCSV" ^
    --release-label emr-6.0.0 ^
    --applications Name=Spark ^
    --log-uri s3://pyspark-sunil/logs/ ^
    --ec2-attributes KeyName=sunil-aws-emr-key-pair-east1 ^
    --instance-type m4.large ^
    --instance-count 2 ^
    --bootstrap-actions Path=s3://pyspark-sunil/emr_bootstrap.sh ^
    --steps Type=Spark,Name="Spark-Job-RunCSV",ActionOnFailure=CONTINUE,Args=[--deploy-mode,client,--master,yarn,s3://pyspark-sunil/run/pyspark-csv.py,s3://pyspark-sunil/run/pyspark-csv.properties] ^
    --use-default-roles ^
    --auto-terminate

rem Check Status
aws emr list-clusters

rem Login
rem aws emr ssh --cluster-id j-3SD91U2E1L2QX --key-pair-file ~/.ssh/mykey.pem