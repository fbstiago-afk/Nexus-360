@echo off
cd /d "%~dp0"
copy /b NEXUS360_DB_PARTE_*.bin NEXUS360.db
echo Banco reconstruido: NEXUS360.db
pause
