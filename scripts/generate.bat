@echo off
REM Deep Core Image Generation Script (Windows)
REM Usage: generate.bat "prompt" output.png [ratio] [provider]

if "%~1"=="" (
    echo Usage: generate.bat "prompt" output.png [ratio] [provider]
    echo.
    echo Examples:
    echo   generate.bat "A sunset" sunset.png
    echo   generate.bat "A landscape" landscape.png 16:9
    echo   generate.bat "A cat" cat.png 1:1 qwen-image
    exit /b 1
)

if "%~2"=="" (
    echo Error: Output file is required
    echo Usage: generate.bat "prompt" output.png [ratio] [provider]
    exit /b 1
)

set PROMPT=%~1
set OUTPUT=%~2
set RATIO=%~3
set PROVIDER=%~4

set SCRIPT_DIR=%~dp0

if "%RATIO%"=="" (
    if "%PROVIDER%"=="" (
        python "%SCRIPT_DIR%generate_image.py" --prompt "%PROMPT%" --output "%OUTPUT%"
    ) else (
        python "%SCRIPT_DIR%generate_image.py" --prompt "%PROMPT%" --output "%OUTPUT%" --provider "%PROVIDER%"
    )
) else (
    if "%PROVIDER%"=="" (
        python "%SCRIPT_DIR%generate_image.py" --prompt "%PROMPT%" --output "%OUTPUT%" --ratio "%RATIO%"
    ) else (
        python "%SCRIPT_DIR%generate_image.py" --prompt "%PROMPT%" --output "%OUTPUT%" --ratio "%RATIO%" --provider "%PROVIDER%"
    )
)
