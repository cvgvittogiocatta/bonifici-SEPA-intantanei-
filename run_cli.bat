@echo off
REM =========================================================================
REM SEPA Transfer Manager - Script CLI per Windows
REM =========================================================================
REM Esegui comandi dal terminale in modo facile!
REM =========================================================================

echo.
echo ============================================================================
echo.  ^(^) SEPA Transfer Manager - Interfaccia CLI
echo ============================================================================
echo.

REM Verifica se Python è installato
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRORE] Python non è installato!
    pause
    exit /b 1
)

echo [OK] Python trovato!
echo.

REM Installa dipendenze se necessario
pip install -r requirements.txt >nul 2>&1

echo.
echo Seleziona un comando:
echo.
echo 1 - Visualizza lista bonifici
echo 2 - Invia nuovo bonifico
echo 3 - Visualizza statistiche
echo 4 - Esci
echo.

set /p choice="Scegli (1-4): "

if "%choice%"=="1" (
    python main.py history
) else if "%choice%"=="2" (
    python main.py send
) else if "%choice%"=="3" (
    python main.py stats
) else if "%choice%"=="4" (
    exit /b 0
) else (
    echo Scelta non valida!
)

pause