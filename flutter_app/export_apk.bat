@echo off
set SOURCE=build\app\outputs\flutter-apk\app-release.apk
set DEST=\\192.168.50.203\elements\app-release.apk

if exist "%SOURCE%" (
    copy /Y "%SOURCE%" "%DEST%"
    echo APK exported to %DEST%
) else (
    echo APK not found!
)
