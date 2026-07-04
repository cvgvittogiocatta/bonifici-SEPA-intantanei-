# 🏦 SEPA Transfer Manager - GUIDA RAPIDA MAC/LINUX

## 🚀 AVVIO VELOCE (3 STEP)

### Step 1: Estrai il ZIP
```bash
unzip bonifici-SEPA-intantanei-.zip
cd bonifici-SEPA-intantanei-
```

### Step 2: Dai permessi di esecuzione
```bash
chmod +x run_app.sh
chmod +x run_cli.sh
```

### Step 3: SCEGLI UN OPZIONE

#### 🌐 **Opzione A: Web Dashboard (CONSIGLIATO)**
```bash
./run_app.sh
↓
Apri il browser su: http://localhost:5000
↓
🎉 INTERFACCIA BELLISSIMA - INVIA BONIFICI!
```

#### 💻 **Opzione B: CLI (Terminale)**
```bash
./run_cli.sh
↓
Segui il menu interattivo
↓
1 - Visualizza bonifici
2 - Invia bonifico
3 - Statistiche
```

---

## ⚙️ REQUISITI PRIMA DI INIZIARE

✅ **Python 3.10+** - Verifica:
```bash
python3 --version
```

Se non è installato:
```bash
# Mac
brew install python3

# Linux
sudo apt install python3 python3-pip
```

---

## 🎯 PRIMO BONIFICO REALE

1. **Esegui `./run_app.sh`**
2. **Aspetta che installi le dipendenze** (1-2 minuti)
3. **Apri il browser su `http://localhost:5000`**
4. **Compila il form:**
   ```
   Nome Ordinante: VITTORIO GIOVANNI CATTABRIGA
   IBAN Ordinante: IT60X0542811101000000123456
   Nome Beneficiario: Mario Rossi
   IBAN Beneficiario: IT80R0000000000000000123456
   Importo: 100.00
   Causale: Test bonifico
   Tipo: SEPA Istantaneo ⚡
   ```
5. **Clicca: "Invia Bonifico"**
6. **Vedi il risultato:**
   ```
   ✅ BONIFICO INVIATO CON SUCCESSO!
   Payment ID: 550e8400-e29b-41d4-a716-446655440000
   TRN: TRN-2026-07-04-001
   CRO: CRO-2026-07-04-001
   Importo: € 100,00
   ```

---

## 🔄 FILE PRINCIPALI

```
bonifici-SEPA-intantanei-/
├── run_app.sh           ← ESEGUI QUESTO (Web Dashboard)
├── run_cli.sh           ← ESEGUI QUESTO (CLI)
├── web_app.py           (codice backend)
├── main.py              (entry point CLI)
├── requirements.txt     (dipendenze)
├── templates/
│   └── index.html       (interfaccia web)
└── static/
    └── app.js           (logica web)
```

---

## ❌ TROUBLESHOOTING

### Errore: "Permesso negato"
**Soluzione:**
```bash
chmod +x run_app.sh
chmod +x run_cli.sh
```

### Errore: "Porta 5000 già in uso"
**Soluzione:**
```bash
lsof -i :5000
kill -9 <PID>
```

### Errore: "Modulo non trovato"
**Soluzione:**
```bash
pip3 install -r requirements.txt
```

---

## 📞 SUPPORTO

Problemi? Verifica:
- Python è installato? `python3 --version`
- Sei nella cartella giusta? `ls -la`
- Le dipendenze sono installate? `pip3 list`

---

**Versione:** 1.0.0  
**Status:** ✅ PRODUCTION READY  
**Ultimo aggiornamento:** 4 Luglio 2026
