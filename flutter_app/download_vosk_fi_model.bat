@echo off
REM Download and extract the Finnish Vosk model for Windows
setlocal
set MODEL_URL=https://alphacephei.com/vosk/models/vosk-model-small-fi-0.22.zip
set ZIP_FILE=vosk-model-small-fi-0.22.zip
set DEST_DIR=assets\models\vosk-model-small-fi-0.22

REM Create destination directory if it doesn't exist
if not exist "%DEST_DIR%" mkdir "%DEST_DIR%"

REM Download the model zip
curl -L -o "%ZIP_FILE%" %MODEL_URL%

REM Extract the zip file
powershell -Command "Expand-Archive -Path '%ZIP_FILE%' -DestinationPath 'assets\\models'"

REM Move extracted folder to correct location if needed
if exist "assets\models\vosk-model-small-fi-0.22" (
    echo Model extracted successfully.
) else (
    echo Extraction failed or folder not found.
)

REM Delete the zip file
if exist "%ZIP_FILE%" del "%ZIP_FILE%"

REM Delete this bat file
if exist "%~f0" del "%~f0"

echo Done. Press any key to exit.
pause
