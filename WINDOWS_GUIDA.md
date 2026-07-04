# 🏦 SEPA Transfer Manager - GUIDA RAPIDA WINDOWS

## 🚀 AVVIO VELOCE (3 STEP)

### Step 1: Estrai il ZIP
```
Clicca destro su: bonifici-SEPA-intantanei-.zip
Scegli: "Estrai tutto"
Scegli la cartella
Clicca: "Estrai"
```

### Step 2: Apri la cartella estratta
```
Fai doppio click su: bonifici-SEPA-intantanei-
```

### Step 3: SCEGLI UN OPZIONE

#### 🌐 **Opzione A: Web Dashboard (CONSIGLIATO)**
```
Fai doppio click su: run_app.bat
↓
Si apre il terminale
↓
Apri il browser su: http://localhost:5000
↓
🎉 INTERFACCIA BELLISSIMA - INVIA BONIFICI!
```

#### 💻 **Opzione B: CLI (Terminale)**
```
Fai doppio click su: run_cli.bat
↓
Segui il menu interattivo
↓
1 - Visualizza bonifici
2 - Invia bonifico
3 - Statistiche
```

---

## ⚙️ REQUISITI PRIMA DI INIZIARE

✅ **Python 3.10+** - Scarica da: https://www.python.org/downloads/
   - IMPORTANTE: Spunta "Add Python to PATH" durante l'installazione!

✅ **Git** (opzionale) - Scarica da: https://git-scm.com/download/win

---

## 🎯 PRIMO BONIFICO REALE

1. **Doppio click su `run_app.bat`**
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
├── run_app.bat          ← DOPPIO CLICK QUA (Web Dashboard)
├── run_cli.bat          ← DOPPIO CLICK QUA (CLI)
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

### Errore: "Python non trovato"
**Soluzione:**
1. Scarica Python: https://www.python.org/downloads/
2. Installa con: **"Add Python to PATH" SPUNTATO**
3. Riavvia il PC
4. Riprova

### Errore: "Porta 5000 già in uso"
**Soluzione:**
1. Apri il terminale
2. Esegui: `netstat -ano | findstr :5000`
3. Termina il processo che usa la porta
4. Riprova

### Errore: "Modulo non trovato"
**Soluzione:**
1. Apri il terminale nella cartella
2. Esegui: `pip install -r requirements.txt`
3. Riprova

---

## 📞 SUPPORTO

Problemi? Controlla:
- Python è installato? `python --version`
- Sei nella cartella giusta?
- Le dipendenze sono installate? `pip list`

---

**Versione:** 1.0.0  
**Status:** ✅ PRODUCTION READY  
**Ultimo aggiornamento:** 4 Luglio 2026
