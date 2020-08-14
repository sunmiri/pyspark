APP_HOME_DIR=%APP_HOME_DIR%
echo "APP_HOME_DIR %APP_HOME_DIR%"

set SPARK_HOME=%APP_HOME_DIR%\lib\spark-3.0.0-bin-hadoop3.2
set PATH=%PATH%;%APP_HOME_DIR%\lib\spark-3.0.0-bin-hadoop3.2\bin
set PYTHONPATH=%SPARK_HOME%\python;%SPARK_HOME%\python\lib\py4j-0.10.9-src.zip;%PYTHONPATH%
set PATH=%SPARK_HOME%\python;%PATH%
echo "SPARK_HOME %SPARK_HOME%"
echo "PYTHONPATH; %PYTHONPATH%"
echo "PATH %PATH%"

cd %APP_HOME_DIR%
if [[ -d "%APP_HOME_DIR%\venv" ]]
then
    echo "Sourcing Python Virtual Env"
    %APP_HOME_DIR%\venv\scripts\activate.bat
else
    echo "Creating Virtual Env in current dir %(pwd)"
    python3 -m venv venv
    %APP_HOME_DIR%\venv\scripts\activate.bat
fi
%APP_HOME_DIR%\venv\scripts\activate.bat
python --version
pip --version
pip install pyspark jproperties argparse