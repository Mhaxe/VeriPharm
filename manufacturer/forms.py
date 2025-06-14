from django import forms
from .models import Batch, BatchDistribution,Drug

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['batch_id','drug_name','drug_category', 'quantity','manufacture_date', 'expiry_date', ]
        widgets = {
            'manufacture_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

class BatchDistributionForm(forms.ModelForm):
    class Meta:
        model = BatchDistribution
        fields = ['batch', 'distributor', 'quantity_sent']

class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = ['name', 'batch']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'batch': forms.Select(attrs={'class': 'form-control'}),
        }