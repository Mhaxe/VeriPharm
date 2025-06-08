from django import forms
from .models import Batch, BatchDistribution,Drug

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['batch_id','drug_name', 'manufacture_date', 'expiry_date', 'total_quantity']
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
        fields = []