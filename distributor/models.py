from django.conf import settings
from django.db import models
from manufacturer.models import Batch

class PharmacyDistribution(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    distributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'distributor'})
    pharmacy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pharmacy_distributions', limit_choices_to={'role': 'pharmacy'})
    quantity_sent = models.PositiveIntegerField()
    sent_date = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity_sent} units to {self.pharmacy.username}"
