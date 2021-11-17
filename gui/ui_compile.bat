FOR %%i IN (*.ui) DO echo %%i
FOR /f "delims=" %%f IN ('dir *.ui /b') DO pyuic5 -o %%~nf.py %%f