// ===== VARIABILI GLOBALI =====
let bonifici = [];

// ===== INIZIALIZZAZIONE =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('App caricata correttamente');
    caricaBonificiDaStorage();
    aggiornaStatistiche();
    mostraStorico();
    setupFormListener();
});

// ===== SETUP FORM =====
function setupFormListener() {
    const form = document.getElementById('bonificoForm');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        inviaBonifico();
    });
}

// ===== INVIA BONIFICO =====
function inviaBonifico() {
    const nomeOrdinante = document.getElementById('nomeOrdinante').value.trim();
    const ibanOrdinante = document.getElementById('ibanOrdinante').value.trim().toUpperCase();
    const nomeBeneficiario = document.getElementById('nomeBeneficiario').value.trim();
    const ibanBeneficiario = document.getElementById('ibanBeneficiario').value.trim().toUpperCase();
    const importo = parseFloat(document.getElementById('importo').value);
    const causale = document.getElementById('causale').value.trim();

    // Validazione
    if (!nomeOrdinante || !ibanOrdinante || !nomeBeneficiario || !ibanBeneficiario || !importo || !causale) {
        alert('❌ Per favore compila tutti i campi!');
        return;
    }

    // Validazione IBAN
    if (!validaIBAN(ibanOrdinante)) {
        alert('❌ IBAN Ordinante non valido!');
        return;
    }

    if (!validaIBAN(ibanBeneficiario)) {
        alert('❌ IBAN Beneficiario non valido!');
        return;
    }

    // Validazione Importo
    if (importo <= 0) {
        alert('❌ L\'importo deve essere maggiore di 0!');
        return;
    }

    if (importo > 1000000) {
        alert('❌ Importo troppo alto!');
        return;
    }

    // Crea oggetto bonifico
    const bonifico = {
        id: generaID(),
        nomeOrdinante,
        ibanOrdinante,
        nomeBeneficiario,
        ibanBeneficiario,
        importo,
        causale,
        data: new Date().toLocaleString('it-IT'),
        timestamp: Date.now(),
        status: 'COMPLETATO'
    };

    // Aggiungi alla lista
    bonifici.push(bonifico);

    // Salva in localStorage
    salvaBonificiInStorage();

    // Mostra messaggio di successo
    mostraMessaggioSuccesso();

    // Aggiorna UI
    aggiornaStatistiche();
    mostraStorico();

    // Pulisci form
    document.getElementById('bonificoForm').reset();

    console.log('✅ Bonifico inviato:', bonifico);
}

// ===== VALIDAZIONE IBAN =====
function validaIBAN(iban) {
    // Validazione base IBAN
    if (!iban || iban.length < 15 || iban.length > 34) {
        return false;
    }

    // Deve iniziare con lettere (codice paese)
    if (!/^[A-Z]{2}/.test(iban)) {
        return false;
    }

    // Deve contenere solo lettere e numeri
    if (!/^[A-Z0-9]+$/.test(iban)) {
        return false;
    }

    return true;
}

// ===== GENERA ID UNIVOCO =====
function generaID() {
    return 'SEPA_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// ===== MESSAGGIO SUCCESSO =====
function mostraMessaggioSuccesso() {
    const form = document.querySelector('.bonifico-form');
    const messaggio = document.createElement('div');
    messaggio.className = 'success-message';
    messaggio.textContent = '✅ Bonifico SEPA inviato correttamente!';
    
    form.insertBefore(messaggio, form.firstChild);

    setTimeout(() => {
        messaggio.remove();
    }, 5000);
}

// ===== AGGIORNA STATISTICHE =====
function aggiornaStatistiche() {
    // Totale bonifici
    const totalBonifici = bonifici.length;
    document.getElementById('totalBonifici').textContent = totalBonifici;

    // Importo totale
    const importoTotale = bonifici.reduce((sum, b) => sum + b.importo, 0);
    document.getElementById('importoTotale').textContent = '€ ' + importoTotale.toFixed(2).replace('.', ',');

    // Importo medio
    const importoMedio = totalBonifici > 0 ? importoTotale / totalBonifici : 0;
    document.getElementById('importoMedio').textContent = '€ ' + importoMedio.toFixed(2).replace('.', ',');
}

// ===== MOSTRA STORICO =====
function mostraStorico() {
    const container = document.getElementById('storicoContainer');
    container.innerHTML = '';

    if (bonifici.length === 0) {
        container.innerHTML = '<p class="empty-message">Nessun bonifico registrato. Invia il tuo primo bonifico!</p>';
        return;
    }

    // Ordina per data decrescente (più recente per primo)
    const bonificiOrdinati = [...bonifici].sort((a, b) => b.timestamp - a.timestamp);

    bonificiOrdinati.forEach((bonifico, index) => {
        const item = document.createElement('div');
        item.className = 'storico-item';
        item.innerHTML = `
            <div class="storico-header">
                <div>
                    <div class="storico-nominativo">${index + 1}. ${bonifico.nomeBeneficiario}</div>
                    <div class="storico-data">📅 ${bonifico.data}</div>
                </div>
                <div class="storico-importo">€ ${bonifico.importo.toFixed(2).replace('.', ',')}</div>
            </div>
            <div class="storico-causale">
                <strong>Causale:</strong> ${bonifico.causale}
            </div>
            <div class="storico-iban">
                <strong>Da:</strong> ${bonifico.ibanOrdinante}<br>
                <strong>A:</strong> ${bonifico.ibanBeneficiario}
            </div>
            <div class="storico-iban">
                <strong>Status:</strong> <span style="color: #10b981; font-weight: bold;">✅ ${bonifico.status}</span>
            </div>
        `;
        container.appendChild(item);
    });
}

// ===== SALVA IN LOCAL STORAGE =====
function salvaBonificiInStorage() {
    try {
        localStorage.setItem('sepa_bonifici', JSON.stringify(bonifici));
        console.log('💾 Dati salvati in localStorage');
    } catch (error) {
        console.error('❌ Errore salvataggio:', error);
    }
}

// ===== CARICA DA LOCAL STORAGE =====
function caricaBonificiDaStorage() {
    try {
        const dati = localStorage.getItem('sepa_bonifici');
        if (dati) {
            bonifici = JSON.parse(dati);
            console.log('📂 Dati caricati da localStorage:', bonifici.length, 'bonifici');
        }
    } catch (error) {
        console.error('❌ Errore caricamento:', error);
        bonifici = [];
    }
}

// ===== FUNZIONI AGGIUNTIVE =====

// Esporta bonifici come JSON
function esportaBonifici() {
    const dataStr = JSON.stringify(bonifici, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'bonifici-' + new Date().toISOString().slice(0, 10) + '.json';
    link.click();
    console.log('📥 Bonifici esportati');
}

// Azzera storico
function azzerapStorico() {
    if (confirm('⚠️ Sei sicuro? Questo eliminerà tutti i bonifici!')) {
        bonifici = [];
        salvaBonificiInStorage();
        aggiornaStatistiche();
        mostraStorico();
        alert('✅ Storico eliminato');
        console.log('🗑️ Storico azzarato');
    }
}

// Log informazioni app
console.log('%c=== SEPA Transfer Manager ===', 'color: #2563eb; font-size: 16px; font-weight: bold;');
console.log('%cVersione: 1.0.0 Web Edition', 'color: #10b981; font-size: 12px;');
console.log('%cApp caricata e pronta all\'uso!', 'color: #059669; font-size: 12px;');
console.log('%cTotalte bonifici caricati: ' + bonifici.length, 'color: #f59e0b; font-size: 12px;');
