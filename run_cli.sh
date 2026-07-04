#!/bin/bash

# =========================================================================
# SEPA Transfer Manager - Script CLI per Mac/Linux
# =========================================================================
# Esegui comandi dal terminale in modo facile!
# =========================================================================

echo ""
echo "============================================================================"
echo "  🏦 SEPA Transfer Manager - Interfaccia CLI"
echo "============================================================================"
echo ""

# Verifica se Python è installato
if ! command -v python3 &> /dev/null; then
    echo "[ERRORE] Python non è installato!"
    exit 1
fi

echo "[OK] Python trovato!"
echo ""

# Installa dipendenze se necessario
pip3 install -r requirements.txt > /dev/null 2>&1

echo ""
echo "Seleziona un comando:"
echo ""
echo "1 - Visualizza lista bonifici"
echo "2 - Invia nuovo bonifico"
echo "3 - Visualizza statistiche"
echo "4 - Esci"
echo ""

read -p "Scegli (1-4): " choice

case $choice in
    1)
        python3 main.py history
        ;;
    2)
        python3 main.py send
        ;;
    3)
        python3 main.py stats
        ;;
    4)
        exit 0
        ;;
    *)
        echo "Scelta non valida!"
        ;;
esac