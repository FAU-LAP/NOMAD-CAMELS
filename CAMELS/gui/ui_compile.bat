FOR /f "delims=" %%f IN ('dir *.ui /b') DO (
call pyuic5 -o %%~nf.py %%f
)
cd ../tools
FOR /f "delims=" %%f IN ('dir *.ui /b') DO (
call pyuic5 -o %%~nf.py %%f
)
cd ../add_ons
for /f "delims==" %%d in ('dir /b') do (
    if exist %%d\*.ui (
        cd %%d
        for /f "delims=" %%f in ('dir *.ui /b') do (
            call pyuic5 -o %%~nf.py %%f
        )
        cd ..
    )
)
cd ../devices/devices_drivers
for /f "delims==" %%d in ('dir /b') do (
    if exist %%d\*.ui (
        cd %%d
        for /f "delims=" %%f in ('dir *.ui /b') do (
            call pyuic5 -o %%~nf.py %%f
        )
        cd ..
    )
)
cd ../..
cd ..\..\PycharmProjects\CAMELS_installer\gui\
FOR /f "delims=" %%f IN ('dir *.ui /b') DO (
call pyuic5 -o %%~nf.py %%f
)