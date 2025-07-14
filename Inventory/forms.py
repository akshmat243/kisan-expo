from django import forms
from .models import StockTransaction, StockTransfer

class StockTransactionForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = ['product', 'warehouse', 'transaction_type', 'quantity', 'note']

class StockTransferForm(forms.ModelForm):
    class Meta:
        model = StockTransfer
        fields = ['product', 'from_warehouse', 'to_warehouse', 'quantity']