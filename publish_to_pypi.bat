@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo FSTDB PyPI 배포 스크립트
echo ========================================
echo.

REM 필요한 도구 확인
echo [1단계] 필요한 도구 확인 중...
python -c "import build" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo build 모듈이 설치되지 않았습니다. 설치 중...
    python -m pip install --upgrade build
    if %ERRORLEVEL% NEQ 0 (
        echo build 설치 실패!
        pause
        exit /b 1
    )
)

python -c "import twine" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo twine 모듈이 설치되지 않았습니다. 설치 중...
    python -m pip install --upgrade twine
    if %ERRORLEVEL% NEQ 0 (
        echo twine 설치 실패!
        pause
        exit /b 1
    )
)
echo   ✓ 필요한 도구 확인 완료
echo.

REM 기존 빌드 파일 정리
echo [2단계] 기존 빌드 파일 정리 중...
if exist dist (
    echo   기존 dist 폴더 삭제 중...
    rmdir /s /q dist
)
if exist build (
    echo   기존 build 폴더 삭제 중...
    rmdir /s /q build
)
if exist *.egg-info (
    echo   기존 egg-info 폴더 삭제 중...
    rmdir /s /q *.egg-info
)
echo   ✓ 정리 완료
echo.

REM 패키지 빌드
echo [3단계] 패키지 빌드 중...
python -m build
if %ERRORLEVEL% NEQ 0 (
    echo 빌드 실패!
    pause
    exit /b 1
)
echo   ✓ 빌드 완료
echo.

REM 빌드 파일 확인
echo [4단계] 빌드 파일 확인 중...
if not exist dist (
    echo dist 폴더가 생성되지 않았습니다!
    pause
    exit /b 1
)
dir /b dist
echo   ✓ 빌드 파일 확인 완료
echo.

REM 업로드 대상 선택
echo ========================================
echo 업로드 대상 선택
echo ========================================
echo 1. TestPyPI (테스트용)
echo 2. PyPI (실제 배포)
echo.
set /p choice="선택 (1 또는 2): "

if "%choice%"=="1" (
    set REPO=--repository testpypi
    set REPO_NAME=TestPyPI
) else if "%choice%"=="2" (
    set REPO=
    set REPO_NAME=PyPI
) else (
    echo 잘못된 선택입니다!
    pause
    exit /b 1
)

echo.
echo ========================================
echo %REPO_NAME%에 업로드할 파일:
echo ========================================
dir /b dist
echo.

REM 최종 확인
set /p confirm="%REPO_NAME%에 업로드하시겠습니까? (y/n): "
if /i not "%confirm%"=="y" (
    echo 업로드가 취소되었습니다.
    pause
    exit /b 0
)

echo.
echo [5단계] %REPO_NAME%에 업로드 중...
python -m twine upload %REPO% dist/*
if %ERRORLEVEL% NEQ 0 (
    echo 업로드 실패!
    pause
    exit /b 1
)

echo.
echo ========================================
echo 업로드 완료!
echo ========================================
echo.
echo 설치 방법:
if "%choice%"=="1" (
    echo   pip install --index-url https://test.pypi.org/simple/ fstdb
) else (
    echo   pip install fstdb
)
echo.
pause
