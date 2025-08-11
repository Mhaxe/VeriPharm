from django import forms
from .models import Batch, BatchDistribution,Drug
from datetime import date
from accounts.models import CustomUser

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['batch_id','drug_name','drug_category', 'quantity','manufacture_date', 'expiry_date', ]
        widgets = {
            'manufacture_date': forms.HiddenInput,
            'expiry_date': forms.HiddenInput,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: Remove required from the hidden date fields, since you're replacing them
        self.fields['manufacture_date'].required = False
        self.fields['expiry_date'].required = False
        

    def clean(self):
        cleaned_data = super().clean()

        # Get individual date parts from self.data (raw POST, not cleaned_data)
        try:
            mfg_day = int(self.data.get('manufacture_day'))
            mfg_month = int(self.data.get('manufacture_month'))
            mfg_year = int(self.data.get('manufacture_year'))
            manufacture_date = date(mfg_year, mfg_month, mfg_day)
            cleaned_data['manufacture_date'] = manufacture_date
        except Exception:
            self.add_error(None, "Invalid manufacture date")

        try:
            exp_day = int(self.data.get('expiry_day'))
            exp_month = int(self.data.get('expiry_month'))
            exp_year = int(self.data.get('expiry_year'))
            expiry_date = date(exp_year, exp_month, exp_day)
            cleaned_data['expiry_date'] = expiry_date
        except Exception:
            self.add_error(None, "Invalid expiry date")

        # Check expiry date after manufacture date
        if 'manufacture_date' in cleaned_data and 'expiry_date' in cleaned_data:
            try:
                if cleaned_data['expiry_date'] < cleaned_data['manufacture_date']:
                    self.add_error('expiry_date', "Expiry date cannot be earlier than manufacture date.")
            except(TypeError):
                pass     

        return cleaned_data    

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

class CodeForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['batch_id']