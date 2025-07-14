from django.contrib import admin
from .models import (
    Account, Contact, Lead, Opportunity, Activity,
    OpportunityNote, Document
)


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 0


class OpportunityNoteInline(admin.TabularInline):
    model = OpportunityNote
    extra = 1

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'phone', 'website', 'created_at')
    search_fields = ('name', 'industry', 'phone', 'website')
    list_filter = ('industry', 'created_at')
    inlines = [ContactInline]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'position', 'account', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'position')
    list_filter = ('position', 'created_at')
    autocomplete_fields = ['account']

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'source', 'status', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'source')
    list_filter = ('status', 'source', 'created_at')

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'account', 'contact', 'value', 'stage', 'expected_close_date', 'created_at')
    search_fields = ('name', 'description', 'account__name')
    list_filter = ('stage', 'expected_close_date', 'created_at')
    autocomplete_fields = ['account', 'contact']
    inlines = [OpportunityNoteInline]

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_type', 'subject', 'account', 'contact', 'due_date', 'status', 'created_by')
    search_fields = ('subject', 'notes')
    list_filter = ('activity_type', 'status', 'due_date')
    autocomplete_fields = ['account', 'contact', 'created_by']

@admin.register(OpportunityNote)
class OpportunityNoteAdmin(admin.ModelAdmin):
    list_display = ('opportunity', 'author', 'created_at')
    search_fields = ('content', 'opportunity__name')
    list_filter = ('created_at',)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'account', 'uploaded_by', 'uploaded_at')
    search_fields = ('name', 'description')
    list_filter = ('uploaded_at',)
    autocomplete_fields = ['account', 'uploaded_by']
