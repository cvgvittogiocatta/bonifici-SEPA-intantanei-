@echo off
REM =========================================================================
REM SEPA Transfer Manager - Script di avvio automatico per Windows
REM =========================================================================
REM Con doppio click installa le dipendenze e lancia l'app!
REM =========================================================================

echo.
echo ============================================================================
echo.  ^(^) SEPA Transfer Manager - Bonifici SEPA Istantanei
echo ============================================================================
echo.

REM Verifica se Python è installato
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERRORE] Python non è installato!
    echo.
    echo Scarica Python da: https://www.python.org/downloads/
    echo Assicurati di spuntare "Add Python to PATH" durante l'installazione
    echo.
    pause
    exit /b 1
)

echo [OK] Python trovato!
echo.

REM Verifica se Git è installato
git --version >nul 2>&1
if errorlevel 1 (
    echo [AVVISO] Git non trovato, ma non serve per eseguire l'app
)

echo.
echo [1/3] Installazione dipendenze...
echo.

REM Installa le dipendenze
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERRORE] Errore nell'installazione delle dipendenze!
    echo.
    pause
    exit /b 1
)

echo.
echo [2/3] Dipendenze installate!
echo.

REM Inizializza il database
echo [3/3] Inizializzazione database...
echo.

python -c "from database import init_db; init_db(); print('[OK] Database pronto!')"

if errorlevel 1 (
    echo.
    echo [AVVISO] Errore nell'inizializzazione del database
    echo.
)

echo.
echo ============================================================================
echo.
echo [^) AVVIO WEB DASHBOARD...
echo.
echo Apri il browser su: http://localhost:5000
echo.
echo Premi CTRL+C nel terminale per fermare il server
echo.
echo ============================================================================
echo.

REM Avvia l'app
python web_app.py

if errorlevel 1 (
    echo.
    echo [ERRORE] Errore nell'avvio dell'applicazione!
    echo.
    pause
)

pause