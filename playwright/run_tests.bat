@echo off
:: Step 1: Check if Python is installed
python --version
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python and try again.
    exit /b 1
)

:: Step 2: Install dependencies from requirements.txt
echo Installing dependencies...
pip install -r requirements.txt

:: Step 3: Install Playwright and browsers
echo Installing Playwright and required browsers...
playwright install

:: Step 4: Run the test suite with pytest and generate HTML report
echo Running tests and generating HTML report...
pytest tests/ --html=traces/report.html --self-contained-html

:: Step 5: Check if the tests were successful
IF %ERRORLEVEL% NEQ 0 (
    echo Tests failed. Please check the report for errors.
    exit /b 1
)

:: Step 6: Optional - Run tests with Playwright trace recording enabled
:: Check if trace files were generated in the 'traces' folder
if exist traces\*.zip (
    echo Trace files found, opening the trace viewer...
    playwright show-trace traces\*.zip
) else (
    echo No trace files found. Please check the test execution for errors.
)

:: Pause to view output
pause