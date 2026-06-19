@echo off
python -m pytest -v --junitxml="..\Execution Report\junit_results.xml"
pause
