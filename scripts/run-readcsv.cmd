set APP_HOME_DIR=%APP_HOME_DIR%
cd %APP_HOME_DIR%
echo "JAVA_HOME %JAVA_HOME%"
echo "SPARK_HOME %SPARK_HOME%"
echo "PATH %PATH%"

echo "Starting Program"
cd %APP_HOME_DIR%\src\python\
rem Option;1
%SPARK_HOME%\bin\spark-submit --master local[4] --jars "%APP_HOME_DIR%\lib\spark-streaming-kinesis-asl-assembly_2.12-3.0.0.jar,%APP_HOME_DIR%\lib\spark-avro_2.12-3.0.0.jar" %APP_HOME_DIR%\src\python\pyspark-csv.py --p %APP_HOME_DIR%\scripts\pyspark-csv.properties

rem Option;2
rem pyspark pyspark-csv.py %APP_HOME_DIR%\src\python\pyspark-csv.properties