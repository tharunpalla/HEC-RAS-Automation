set "VORTEX_HOME=C:\Programs\vortex-0.10.16"
set "JAVA_HOME=C:\Users\chand\Downloads\OpenJDK11U-jdk_x64_windows_hotspot_11.0.14_9\jdk-11.0.14+9"
set "PATH=%VORTEX_HOME%\bin;%VORTEX_HOME%\bin\gdal;%JAVA_HOME%\bin;%PATH%"
set "GDAL_DATA=%VORTEX_HOME%\bin\gdal\gdal-data"
set "PROJ_LIB=%VORTEX_HOME%\bin\gdal\projlib"
set "CLASSPATH=%VORTEX_HOME%\lib\*"
C:\Programs\jython2.7.2\bin\jython.exe -J-Xmx2g -Djava.library.path=%VORTEX_HOME%\bin;%VORTEX_HOME%\bin\gdal -Dpython.path='C:\Users\chand\AppData\Local\Programs\Python\Python39' grid_to_point_Converter.py