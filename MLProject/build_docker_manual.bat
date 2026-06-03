@echo off
REM Manual Docker Build Script for Heart Disease Model
REM This script builds the Docker image using mlflow build-docker function

echo ========================================
echo MLflow Docker Build Script
echo ========================================
echo.

REM Set required environment variables
set MLFLOW_ALLOW_FILE_STORE=true
set MLFLOW_TRACKING_URI=./mlruns

echo Setting environment variables...
echo MLFLOW_ALLOW_FILE_STORE=%MLFLOW_ALLOW_FILE_STORE%
echo MLFLOW_TRACKING_URI=%MLFLOW_TRACKING_URI%
echo.

echo Checking Docker Desktop status...
docker info >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker Desktop is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)
echo Docker Desktop is running.
echo.

echo Checking internet connectivity to GitHub...
ping -n 1 github.com >nul 2>&1
if errorlevel 1 (
    echo WARNING: Cannot reach GitHub. This may cause Docker build to fail.
    echo Please check your internet connection.
    echo.
    set /p CONTINUE="Do you want to continue anyway? (Y/N): "
    if /i not "%CONTINUE%"=="Y" exit /b 1
)
echo.

echo Building Docker image using MLflow...
echo Model: models:/heart-disease-classifier/6
echo Image: f4rma/heart-disease-model:latest
echo.
echo This may take 5-10 minutes...
echo.

python -m mlflow models build-docker -m "models:/heart-disease-classifier/6" -n "f4rma/heart-disease-model:latest"

if errorlevel 1 (
    echo.
    echo ERROR: Docker build failed!
    echo.
    echo Common issues:
    echo 1. Network connectivity problems - Cannot reach GitHub
    echo 2. Docker Desktop not running
    echo 3. Insufficient disk space
    echo.
    echo Please fix the issue and run this script again.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Docker image built successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Login to Docker Hub: docker login
echo    Username: f4rma
echo    Password: [Your Docker Hub Token]
echo.
echo 2. Push image: docker push f4rma/heart-disease-model:latest
echo.
echo 3. Verify on Docker Hub: https://hub.docker.com/r/f4rma/heart-disease-model
echo.
pause
