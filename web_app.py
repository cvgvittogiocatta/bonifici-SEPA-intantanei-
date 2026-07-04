from flask import Flask, render_template, request, jsonify
from datetime import datetime
from decimal import Decimal
import json
import os
from database import SessionLocal, SEPATransferDB
from models import SEPATransferRequest, Account, Party
from transfer_manager import TransferManager

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
def index():
    """Home page - Web Dashboard"""
    return render_template('index.html')

@app.route('/api/transfers', methods=['GET'])
def get_transfers():
    """Ottieni storico bonifici"""
    try:
        db = SessionLocal()
        transfers = db.query(SEPATransferDB).order_by(SEPATransferDB.created_at.desc()).limit(50).all()
        db.close()
        
        data = [{
            'id': t.id,
            'message_id': t.message_id,
            'payment_id': t.payment_id,
            'initiating_party_name': t.initiating_party_name,
            'initiating_party_iban': t.initiating_party_iban,
            'recipient_name': t.recipient_name,
            'recipient_iban': t.recipient_iban,
            'amount': float(t.amount),
            'currency': t.currency,
            'status': t.status.value,
            'transaction_id': t.transaction_id,
            'creditor_reference': t.creditor_reference,
            'created_at': t.created_at.isoformat(),
            'transfer_type': t.transfer_type.value
        } for t in transfers]
        
        return jsonify({'success': True, 'data': data, 'count': len(data)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/transfer/send', methods=['POST'])
def send_transfer():
    """Invia bonifico SEPA"""
    try:
        data = request.get_json()
        
        # Validazione dati
        required = ['sender_iban', 'sender_name', 'recipient_iban', 'recipient_name', 'amount']
        if not all(k in data for k in required):
            return jsonify({'success': False, 'error': 'Dati mancanti'}), 400
        
        # Crea transfer request
        transfer_request = SEPATransferRequest(
            initiating_party=Party(
                name=data['sender_name'],
                account=Account(iban=data['sender_iban'])
            ),
            recipient=Party(
                name=data['recipient_name'],
                account=Account(iban=data['recipient_iban'])
            ),
            amount=Decimal(str(data['amount'])),
            currency=data.get('currency', 'EUR'),
            remittance_information=data.get('reason', ''),
            is_instant=data.get('is_instant', True)
        )
        
        # Invia bonifico
        manager = TransferManager()
        response = manager.create_and_send_transfer(transfer_request)
        manager.close()
        
        return jsonify({
            'success': True,
            'payment_id': response.payment_id,
            'message_id': response.message_id,
            'transaction_id': response.transaction_id,
            'creditor_reference': response.creditor_reference,
            'amount': float(response.amount),
            'status': response.status
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Statistiche bonifici"""
    try:
        db = SessionLocal()
        total = db.query(SEPATransferDB).count()
        completed = db.query(SEPATransferDB).filter_by(status='COMPLETED').count()
        total_amount = db.query(SEPATransferDB).all()
        amount_sum = sum(float(t.amount) for t in total_amount)
        db.close()
        
        return jsonify({
            'success': True,
            'total_transfers': total,
            'completed': completed,
            'total_amount': round(amount_sum, 2),
            'currency': 'EUR'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/transfer/<int:transfer_id>', methods=['GET'])
def get_transfer_detail(transfer_id):
    """Dettagli singolo bonifico"""
    try:
        db = SessionLocal()
        transfer = db.query(SEPATransferDB).filter_by(id=transfer_id).first()
        db.close()
        
        if not transfer:
            return jsonify({'success': False, 'error': 'Bonifico non trovato'}), 404
        
        return jsonify({
            'success': True,
            'data': {
                'id': transfer.id,
                'message_id': transfer.message_id,
                'payment_id': transfer.payment_id,
                'initiating_party_name': transfer.initiating_party_name,
                'initiating_party_iban': transfer.initiating_party_iban,
                'recipient_name': transfer.recipient_name,
                'recipient_iban': transfer.recipient_iban,
                'amount': float(transfer.amount),
                'currency': transfer.currency,
                'status': transfer.status.value,
                'transaction_id': transfer.transaction_id,
                'creditor_reference': transfer.creditor_reference,
                'remittance_information': transfer.remittance_information,
                'created_at': transfer.created_at.isoformat(),
                'transfer_type': transfer.transfer_type.value
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🚀 SEPA Transfer Manager - Web Dashboard")
    print("="*80)
    print("\n🌐 Apri nel browser: http://localhost:5000")
    print("\n📝 Invia bonifici istantanei REALI dal tuo browser!")
    print("\n" + "="*80 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)