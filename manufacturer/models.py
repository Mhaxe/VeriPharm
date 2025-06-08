from django.db import models

# Create your models here.
# models.py
from django.db import models
from django.conf import settings

class Batch(models.Model):
    batch_id = models.CharField(max_length=100)
    drug_name = models.CharField(max_length=100)
    manufacturer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    manufacture_date = models.DateField()
    expiry_date = models.DateField()

    def __str__(self):
        return self.name

class Drug(models.Model):
    name = models.CharField(max_length=100)
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return self.name
    

class BatchDistribution(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    distributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'distributor'})
    quantity_sent = models.IntegerField()
    distribution_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} units of {self.drug.name} to {self.distributor.username}"
