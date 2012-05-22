setlocal

set JAVA_HOME=C:\Software\jdk1.7.0_03
set JYTHON_HOME=C:\Software\jython2.5.2

set CLASSPATH=%JAVA_HOME%\lib\tools.jar;%CLASSPATH%

%JYTHON_HOME%\jython keytool.py %*

endlocal
