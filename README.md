GIT

1: CLONE (one time)

git clone https://github.com/sunmiri/pyspark.git

2: Get Latest:

cd <your dir>

git pull

3: Check-In & Commit

git status

Will list changes

>>for-each change:

git add <file-with-patch>

>>Once ready to push/commit

git commit -m "some verbose comment"

git remote set-url origin https://sunmiri@github.com/sunmiri/pyspark.git

git push

===========


Api: https://spark.apache.org/docs/latest/api/python/index.html

Run as Py File:
A:
source /opt/codebase/PYTHON3/bin/activate

cd <your-path>/PySpark/

sh ./setenv.sh

echo $SPARK_HOME

cd src/python/

$SPARK_HOME/bin/spark-submit pyspark-local.py

B:

pip install pyspark

python pyspark-local.py

Run on Terminal:

source /opt/codebase/PYTHON3/bin/activate

pip install pyspark

cd <your-path>/PySpark

sh ./setenv.sh

cd <your-path>/PySpark/spark-3.0.0-bin-hadoop3.2/bin

./pyspark --master local[2]

...

...

Using Python version 3.7.3 (v3.7.3:ef4ec6ed12, Mar 25 2019 16:52:21)

SparkSession available as 'spark'.


FAQ:
--SparkStream not reading data from Kinesis
Ans: is kinesis.shards =1 , make sure to start your sparl.local=2. 1:2 ratio

--Caused by: com.amazon.support.exceptions.GeneralException: [Amazon](500150) Error setting/closing connection: Operation timed out
https://github.com/databricks/spark-redshift/issues/160
https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#SecurityGroup:groupId=sg-d5018fee

--SSH
https://console.aws.amazon.com/ec2/home?region=us-east-1#SecurityGroup:group-id=sg-02cd8604cd14b690b
Add Rule -> SSH -> MyIP

--Yarn Logs
>SSH to Master
>yarn application -list
>yarn logs -applicationId application_1597361407286_0001 > ~/application_1597361407286_0001.log
>vi ~/application_1597361407286_0001.log

20/08/13 23:31:55 ERROR ShardSyncTask: Caught exception while sync'ing Kinesis shards and leases
com.amazonaws.services.kinesis.model.AmazonKinesisException: User: arn:aws:sts::962077010122:assumed-role/EMR_EC2_DefaultRole/i-04937587acf6ccf47 is not authorized to perform: kinesis:ListShards on resource: arn:aws:kinesis:us-east-1:962077010122:stream/pyspark-kinesis (Service: AmazonKinesis; Status Code: 400; Error Code: AccessDeniedException; Request ID: d57c3a72-f9fc-ac6c-82d3-f5d8614c8791)
Fix: IAM->Roles->EMR_EC2_DefaultRole -> Attach Policies -> Add "AWSLambdaKinesisExecutionRole" and "AmazonKinesisFullAccess"

--Redshift
processRDD::writing records to AWS Redshift:u:awsuser,p:Training2020,t:public.testtable,j:jdbc:redshift://pyspark-redshift.cui3tprwjwcc.us-east-1.redshift.amazonaws.com:5439/dev?ssl=true&sslfactory=com.amazon.redshift.ssl.NonValidatingFactory
processRDD::Exception writing the df: DataFrame[message: string, number: int] An error occurred while calling o7724.save.
: java.lang.ClassNotFoundException: com.amazon.redshift.jdbc42.Driver
