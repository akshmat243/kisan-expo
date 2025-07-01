from django import forms
from .models import RoleModelPermission


class RoleModelPermissionForm(forms.ModelForm):
    class Meta:
        model = RoleModelPermission
        fields = ['role', 'model', 'permission_type']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
            'model': forms.Select(attrs={'class': 'form-control'}),
            'permission_type': forms.Select(attrs={'class': 'form-control'}),
        }
