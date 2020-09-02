set APP_HOME_DIR=%APP_HOME_DIR%
cd %APP_HOME_DIR%
echo "JAVA_HOME %JAVA_HOME%"
echo "SPARK_HOME %SPARK_HOME%"
echo "PATH %PATH%"

echo "Starting Program"
cd %APP_HOME_DIR%\src\python\
rem Option;1
%SPARK_HOME%\bin\spark-submit --master local[4] --jars "%APP_HOME_DIR%\lib\spark-streaming-kafka-0-10_2.12-3.0.0.jar,%APP_HOME_DIR%\lib\spark-sql-kafka-0-10_2.12-3.0.0.jar,%APP_HOME_DIR%\lib\spark-avro_2.12-3.0.0.jar,%APP_HOME_DIR%\lib\RedshiftJDBC42-no-awssdk-1.2.45.1069.jar,%APP_HOME_DIR%\lib\kafka-clients-2.4.1.jar" %APP_HOME_DIR%\src\python\pyspark-kafka.py --p %APP_HOME_DIR%\scripts\pyspark-kafka.properties

rem Option;2
rem pyspark pyspark-csv.py %APP_HOME_DIR%\src\python\pyspark-csv.properties