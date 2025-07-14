from django import forms
from .models import (
    Account, Contact, Lead, Opportunity,
    Activity, OpportunityNote, Document
)

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'industry', 'website', 'phone', 'address', 'description']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['account', 'full_name', 'email', 'phone', 'position', 'notes']

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['full_name', 'email', 'phone', 'source', 'status', 'interested_product', 'notes']

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ['name', 'account', 'contact', 'value', 'stage', 'expected_close_date', 'description']

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['activity_type', 'subject', 'account', 'contact', 'due_date', 'status', 'notes']

class OpportunityNoteForm(forms.ModelForm):
    class Meta:
        model = OpportunityNote
        fields = ['opportunity', 'content']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['account', 'file', 'name', 'description']