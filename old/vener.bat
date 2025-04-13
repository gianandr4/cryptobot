@echo off
setlocal

:: Set default path to current directory
set "Path=%~1"
if "%Path%"=="" set "Path=%cd%"

:: Function to activate a virtual environment
call :ActivateVenv "%Path%"

:: Check if .venv exists and activate it
if exist "%Path%\venv\Scripts\activate.bat" (
    call "%Path%\venv\Scripts\activate.bat"
) else (
    :: Look for requirements.txt in the current directory
    if exist "%Path%\requirements.txt" (
        set "DirName=%~nx1"
        echo Creating new virtual environment named "%DirName%"...
        python -m venv "%Path%\%DirName%"
        call "%Path%\%DirName%\Scripts\activate.bat"
        pip install -r "%Path%\requirements.txt"
        echo Dependencies installed successfully!
    ) else (
        echo Error: No .venv or requirements.txt found in the specified directory.
    )
)

:: Exit function if not activated
goto :eof

:ActivateVenv
:: Check if the virtual environment exists in the path
if exist "%1\.venv\Scripts\activate.bat" (
    call "%1\.venv\Scripts\activate.bat"
    echo Virtual environment activated.
) else (
    echo No .venv found in the specified directory.
)
goto :eof
