# SEPA Transfer Manager - Main Kivy App

import os
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.core.window import Window
from decimal import Decimal
import requests
import json
from datetime import datetime

# Impostazioni finestra
Window.size = (400, 800)
Window.title = 'SEPA Transfer Manager'

class SEPATransferApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transfers = []
        self.api_url = 'http://localhost:5000'
        
    def build(self):
        self.title = 'SEPA Transfer Manager - Bonifici SEPA Istantanei'
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # HEADER
        header = Label(
            text='[b]🏦 SEPA Transfer Manager[/b]\nBonifici SEPA Istantanei Reali',
            markup=True,
            size_hint_y=0.1,
            bold=True
        )
        main_layout.add_widget(header)
        
        # STATISTICHE
        stats_layout = GridLayout(cols=3, size_hint_y=0.15, spacing=5)
        self.stat_total = Label(text='[b]0[/b]\nTotali', markup=True)
        self.stat_completed = Label(text='[b]0[/b]\nCompletati', markup=True)
        self.stat_amount = Label(text='€ [b]0,00[/b]\nImporto', markup=True)
        stats_layout.add_widget(self.stat_total)
        stats_layout.add_widget(self.stat_completed)
        stats_layout.add_widget(self.stat_amount)
        main_layout.add_widget(stats_layout)
        
        # FORM BONIFICO
        form_scroll = ScrollView(size_hint_y=0.55)
        form_layout = GridLayout(cols=1, spacing=5, size_hint_y=None, height=400)
        form_layout.bind(minimum_height=form_layout.setter('height'))
        
        # Input fields
        self.sender_name = TextInput(hint_text='Nome Ordinante', multiline=False, size_hint_y=None, height=40)
        self.sender_iban = TextInput(hint_text='IBAN Ordinante', multiline=False, size_hint_y=None, height=40)
        self.recipient_name = TextInput(hint_text='Nome Beneficiario', multiline=False, size_hint_y=None, height=40)
        self.recipient_iban = TextInput(hint_text='IBAN Beneficiario', multiline=False, size_hint_y=None, height=40)
        self.amount = TextInput(hint_text='Importo (EUR)', multiline=False, size_hint_y=None, height=40, input_filter='float')
        self.reason = TextInput(hint_text='Causale', multiline=False, size_hint_y=None, height=40)
        
        self.transfer_type = Spinner(
            text='SEPA Istantaneo ⚡',
            values=('SEPA Istantaneo ⚡', 'SEPA Standard 📅'),
            size_hint_y=None,
            height=40
        )
        
        form_layout.add_widget(Label(text='Ordinante:', size_hint_y=None, height=20))
        form_layout.add_widget(self.sender_name)
        form_layout.add_widget(self.sender_iban)
        
        form_layout.add_widget(Label(text='Beneficiario:', size_hint_y=None, height=20))
        form_layout.add_widget(self.recipient_name)
        form_layout.add_widget(self.recipient_iban)
        
        form_layout.add_widget(Label(text='Dettagli:', size_hint_y=None, height=20))
        form_layout.add_widget(self.amount)
        form_layout.add_widget(self.reason)
        form_layout.add_widget(self.transfer_type)
        
        form_scroll.add_widget(form_layout)
        main_layout.add_widget(form_scroll)
        
        # PULSANTI
        btn_layout = GridLayout(cols=2, size_hint_y=0.1, spacing=5)
        btn_send = Button(text='✅ Invia Bonifico', background_color=(0.4, 0.7, 1, 1))
        btn_send.bind(on_press=self.send_transfer)
        btn_history = Button(text='📋 Storico', background_color=(0.7, 0.4, 1, 1))
        btn_history.bind(on_press=self.show_history)
        btn_layout.add_widget(btn_send)
        btn_layout.add_widget(btn_history)
        main_layout.add_widget(btn_layout)
        
        # Carica statistiche
        self.load_stats()
        
        return main_layout
    
    def send_transfer(self, instance):
        """Invia bonifico"""
        try:
            data = {
                'sender_name': self.sender_name.text,
                'sender_iban': self.sender_iban.text,
                'recipient_name': self.recipient_name.text,
                'recipient_iban': self.recipient_iban.text,
                'amount': float(self.amount.text) if self.amount.text else 0,
                'reason': self.reason.text,
                'is_instant': 'Istantaneo' in self.transfer_type.text
            }
            
            response = requests.post(f'{self.api_url}/api/transfer/send', json=data, timeout=5)
            result = response.json()
            
            if result.get('success'):
                popup_text = f"✅ Bonifico inviato!\n\nPayment ID: {result.get('payment_id', 'N/A')}\nTRN: {result.get('transaction_id', 'N/A')}\nCRO: {result.get('creditor_reference', 'N/A')}"
                self.show_popup('Successo', popup_text)
                self.clear_form()
                self.load_stats()
            else:
                self.show_popup('Errore', f"Errore: {result.get('error', 'Sconosciuto')}")
        except Exception as e:
            self.show_popup('Errore', f"Errore di connessione: {str(e)}")
    
    def load_stats(self):
        """Carica statistiche"""
        try:
            response = requests.get(f'{self.api_url}/api/stats', timeout=5)
            result = response.json()
            
            if result.get('success'):
                self.stat_total.text = f"[b]{result.get('total_transfers', 0)}[/b]\nTotali"
                self.stat_completed.text = f"[b]{result.get('completed', 0)}[/b]\nCompletati"
                self.stat_amount.text = f"€ [b]{result.get('total_amount', 0):.2f}[/b]\nImporto"
        except:
            pass
    
    def show_history(self, instance):
        """Mostra storico bonifici"""
        try:
            response = requests.get(f'{self.api_url}/api/transfers', timeout=5)
            result = response.json()
            
            if result.get('success'):
                transfers = result.get('data', [])
                content = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None, height=len(transfers)*100)
                
                for t in transfers[:10]:
                    transfer_text = f"💰 {t.get('recipient_name', 'N/A')} - € {t.get('amount', 0):.2f}"
                    content.add_widget(Label(text=transfer_text, size_hint_y=None, height=30))
                
                scroll = ScrollView()
                scroll.add_widget(content)
                
                popup = Popup(title='Storico Bonifici', content=scroll, size_hint=(0.9, 0.8))
                popup.open()
        except:
            self.show_popup('Errore', 'Errore nel caricamento dello storico')
    
    def clear_form(self):
        """Pulisce il form"""
        self.sender_name.text = ''
        self.sender_iban.text = ''
        self.recipient_name.text = ''
        self.recipient_iban.text = ''
        self.amount.text = ''
        self.reason.text = ''
    
    def show_popup(self, title, text):
        """Mostra popup"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=text))
        btn = Button(text='OK', size_hint_y=0.3)
        content.add_widget(btn)
        
        popup = Popup(title=title, content=content, size_hint=(0.9, 0.6))
        btn.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    SEPATransferApp().run()