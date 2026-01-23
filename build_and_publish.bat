@echo off
echo Building FSTDB package...
python -m build

if %ERRORLEVEL% NEQ 0 (
    echo Build failed!
    exit /b 1
)

echo.
echo Build successful! Files are in the dist/ folder.
echo.
echo To upload to PyPI, run:
echo   python -m twine upload dist/*
echo.
echo Or to upload to TestPyPI first:
echo   python -m twine upload --repository testpypi dist/*
echo.

pause
