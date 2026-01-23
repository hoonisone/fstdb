@echo off
echo Installing build package...
python -m pip install --upgrade build
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install build package!
    exit /b 1
)

echo Building package...
python -m build
if %ERRORLEVEL% NEQ 0 (
    echo Build failed!
    exit /b 1
)
echo Build successful! Files are in the dist/ folder.
