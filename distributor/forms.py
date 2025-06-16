from django import forms
from accounts.models import CustomUser
from .models import PharmacyDistribution,Batch


class PharmacyDistributionForm(forms.ModelForm):
    class Meta:
        model = PharmacyDistribution
        fields = ['batch', 'pharmacy', 'quantity_sent']

    def __init__(self, *args, **kwargs):
        distributor = kwargs.pop('distributor', None)
        super().__init__(*args, **kwargs)
        if distributor:
            self.fields['batch'].queryset = Batch.objects.filter(batchdistribution__distributor=distributor)
        self.fields['pharmacy'].queryset = CustomUser.objects.filter(role='pharmacy')
        
