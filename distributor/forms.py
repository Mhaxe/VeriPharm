from django import forms
from accounts.models import CustomUser
from .models import PharmacyDistribution,Batch


class PharmacyDistributionForm(forms.ModelForm):
    class Meta:
        model = PharmacyDistribution
        fields = ['batch', 'pharmacy', 'quantity_sent']

    def __init__(self, *args, **kwargs):
        self.distributor = kwargs.pop('distributor', None)
        super().__init__(*args, **kwargs)
        if self.distributor:
            self.fields['batch'].queryset = Batch.objects.filter(
                batchdistribution__distributor=self.distributor,
                batchdistribution__verified=True
            )
        self.fields['pharmacy'].queryset = CustomUser.objects.filter(
            role='pharmacist'
        ).order_by('username')

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.distributor:
            instance.distributor = self.distributor
        if commit:
            instance.save()
        return instance
