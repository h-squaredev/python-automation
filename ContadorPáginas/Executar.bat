@echo off
cd /d "%~dp0"
python contador_pg.py
if errorlevel 1 pause
