set APP_HOME_DIR=C:\Training\PySpark\pyspark
cd %APP_HOME_DIR%

set JAVA_HOME=C:\Program Files\Java\jdk1.8.0_261

set HADOOP_HOME=%APP_HOME_DIR%\lib\spark-2.4.6-bin-hadoop2.7
set SPARK_HOME=%APP_HOME_DIR%\lib\spark-2.4.6-bin-hadoop2.7
set PATH=%PATH%;%APP_HOME_DIR%\lib\spark-2.4.6-bin-hadoop2.7\bin;%JAVA_HOME%\bin;
set PYTHONPATH=%SPARK_HOME%\python;%SPARK_HOME%\python\lib\py4j-0.10.7-src.zip;%PYTHONPATH%
set PATH=%SPARK_HOME%\python;%PATH%
echo "SPARK_HOME %SPARK_HOME%"
echo "PATH %PATH%"

source $APP_HOME_DIR/venv/bin/activate
python --version
pip --version
pip install pyspark jproperties

cd %APP_HOME_DIR%\src\python\
rem Option;1
%SPARK_HOME%\bin\spark-submit pyspark-csv.py %APP_HOME_DIR%\src\python\pyspark-csv.properties

rem Option;2
rem pyspark pyspark-csv.py %APP_HOME_DIR%\src\python\pyspark-csv.properties