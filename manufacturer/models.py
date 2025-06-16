from django.db import models
from django.conf import settings
import uuid
import qrcode
from io import BytesIO
from django.core.files import File
from .utils import *


class Batch(models.Model):
    batch_id = models.CharField(max_length=100)
    drug_name = models.CharField(max_length=100)
    drug_category = models.CharField(max_length = 100, default = "unknown")
    manufacturer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(max_length=100)
    quantity = models.IntegerField(default=0)
    manufacture_date = models.DateField()
    expiry_date = models.DateField()
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.batch_id
    


class Drug(models.Model):
    name = models.CharField(max_length=100)
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    qr_code_string = models.CharField(max_length=255,unique=True)
    scanned = models.BooleanField(default=False)

    def __str__(self):
        return self.qr_code_string
    
    def save(self, *args, **kwargs):
        self.qr_code_string = generate_qr_code()
        if not self.qr_code:
            qr = qrcode.make(str(self.qr_code_string))
            buffer = BytesIO()
            qr.save(buffer, format='PNG')
            self.qr_code.save(f'{self.qr_code_string}.png', File(buffer), save=False)
        super().save(*args, **kwargs)
    

class BatchDistribution(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    distributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'distributor'})
    quantity_sent = models.IntegerField()
    distribution_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} units of {self.drug.name} to {self.distributor.username}"
