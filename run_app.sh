#!/bin/bash

# =========================================================================
# SEPA Transfer Manager - Script di avvio automatico per Mac/Linux
# =========================================================================
# Con doppio click installa le dipendenze e lancia l'app!
# =========================================================================

echo ""
echo "============================================================================"
echo "  🏦 SEPA Transfer Manager - Bonifici SEPA Istantanei"
echo "============================================================================"
echo ""

# Verifica se Python è installato
if ! command -v python3 &> /dev/null; then
    echo "[ERRORE] Python non è installato!"
    echo ""
    echo "Installa Python da: https://www.python.org/downloads/"
    echo ""
    read -p "Premi Invio per continuare..."
    exit 1
fi

echo "[OK] Python trovato!"
echo ""

echo "[1/3] Installazione dipendenze..."
echo ""

# Installa le dipendenze
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERRORE] Errore nell'installazione delle dipendenze!"
    echo ""
    read -p "Premi Invio per continuare..."
    exit 1
fi

echo ""
echo "[2/3] Dipendenze installate!"
echo ""

# Inizializza il database
echo "[3/3] Inizializzazione database..."
echo ""

python3 -c "from database import init_db; init_db(); print('[OK] Database pronto!')"

echo ""
echo "============================================================================"
echo ""
echo "[⚡] AVVIO WEB DASHBOARD..."
echo ""
echo "Apri il browser su: http://localhost:5000"
echo ""
echo "Premi CTRL+C nel terminale per fermare il server"
echo ""
echo "============================================================================"
echo ""

# Avvia l'app
python3 web_app.py