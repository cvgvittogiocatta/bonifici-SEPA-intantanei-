// Carica statistiche
async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const result = await response.json();
        
        if (result.success) {
            document.getElementById('total-transfers').textContent = result.total_transfers;
            document.getElementById('completed-transfers').textContent = result.completed;
            document.getElementById('total-amount').textContent = `€ ${result.total_amount.toLocaleString('it-IT', {minimumFractionDigits: 2})}`;
        }
    } catch (error) {
        console.error('Errore caricamento stats:', error);
    }
}

// Carica storico bonifici
async function loadTransfers() {
    try {
        const response = await fetch('/api/transfers');
        const result = await response.json();
        const container = document.getElementById('transfers-container');
        
        if (!result.success || result.data.length === 0) {
            container.innerHTML = '<p class="loading">📭 Nessun bonifico ancora</p>';
            return;
        }
        
        let html = '';
        result.data.forEach(transfer => {
            const date = new Date(transfer.created_at).toLocaleString('it-IT');
            const statusClass = transfer.status === 'COMPLETED' ? 'status-completed' : 'status-pending';
            const statusEmoji = transfer.status === 'COMPLETED' ? '✅' : '⏳';
            const typeEmoji = transfer.transfer_type === 'INSTANT' ? '⚡' : '📅';
            
            html += `
                <div class="transfer-item">
                    <div class="transfer-header">
                        <div>
                            <div class="transfer-recipient">${transfer.recipient_name}</div>
                            <div style="font-size: 0.9em; color: #999; margin-top: 5px;">${date}</div>
                        </div>
                        <div style="text-align: right;">
                            <div class="transfer-amount">€ ${transfer.amount.toLocaleString('it-IT', {minimumFractionDigits: 2})}</div>
                            <div style="margin-top: 5px;">
                                <span class="transfer-status ${statusClass}">${statusEmoji} ${transfer.status}</span>
                                <span style="margin-left: 5px; font-size: 0.9em;">${typeEmoji}</span>
                            </div>
                        </div>
                    </div>
                    <div class="transfer-details">
                        <div class="detail-item">
                            <div class="detail-label">📤 Ordinante</div>
                            <div class="detail-value">${transfer.initiating_party_iban}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">📥 Beneficiario</div>
                            <div class="detail-value">${transfer.recipient_iban}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">🆔 Payment ID</div>
                            <div class="detail-value">${transfer.payment_id || 'N/A'}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">📊 TRN</div>
                            <div class="detail-value">${transfer.transaction_id || 'N/A'}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">📎 CRO</div>
                            <div class="detail-value">${transfer.creditor_reference || 'N/A'}</div>
                        </div>
                    </div>
                </div>
            `;
        });
        
        container.innerHTML = html;
    } catch (error) {
        console.error('Errore caricamento bonifici:', error);
        document.getElementById('transfers-container').innerHTML = '<p class="loading">❌ Errore nel caricamento</p>';
    }
}

// Invia bonifico
document.getElementById('transfer-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formStatus = document.getElementById('form-status');
    formStatus.classList.remove('success', 'error');
    formStatus.textContent = '⏳ Invio in corso...';
    formStatus.classList.add('success');
    formStatus.style.display = 'block';
    
    const data = {
        sender_name: document.getElementById('sender_name').value,
        sender_iban: document.getElementById('sender_iban').value,
        recipient_name: document.getElementById('recipient_name').value,
        recipient_iban: document.getElementById('recipient_iban').value,
        amount: parseFloat(document.getElementById('amount').value),
        reason: document.getElementById('reason').value,
        is_instant: document.getElementById('is_instant').value === 'true'
    };
    
    try {
        const response = await fetch('/api/transfer/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            formStatus.classList.remove('error');
            formStatus.classList.add('success');
            formStatus.innerHTML = `
                ✅ <strong>Bonifico inviato con successo!</strong><br>
                Payment ID: ${result.payment_id}<br>
                TRN: ${result.transaction_id}<br>
                CRO: ${result.creditor_reference}
            `;
            
            // Reset form
            document.getElementById('transfer-form').reset();
            
            // Ricarica statistiche e storico
            setTimeout(() => {
                loadStats();
                loadTransfers();
            }, 1000);
        } else {
            formStatus.classList.remove('success');
            formStatus.classList.add('error');
            formStatus.textContent = `❌ Errore: ${result.error}`;
        }
    } catch (error) {
        formStatus.classList.remove('success');
        formStatus.classList.add('error');
        formStatus.textContent = `❌ Errore: ${error.message}`;
    }
});

// Carica al primo avvio
loadStats();
loadTransfers();

// Aggiorna ogni 10 secondi
setInterval(() => {
    loadStats();
    loadTransfers();
}, 10000);