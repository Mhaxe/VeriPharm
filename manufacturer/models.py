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
    quantity_left = models.IntegerField(blank=True, null=True)
    manufacture_date = models.DateField()
    expiry_date = models.DateField()
    batch_qr_code = models.ImageField(upload_to='batch_codes/', blank=True, null=True)
    batch_qr_code_string = models.CharField(max_length=255,unique=True)
    parent_batch = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='sub_batches')
   
    

    def __str__(self):
        return self.batch_id
    
    def save(self, *args, **kwargs):
        if self._state.adding:
            if self.quantity_left is None:
                self.quantity_left = self.quantity

            # Assign a fallback string if batch_id is None
            if not self.batch_qr_code_string:
                self.batch_qr_code_string = str(self.batch_id) or "batch_qr"

        if not self.batch_qr_code:
            qr = qrcode.make(str(self.batch_qr_code_string))
            buffer = BytesIO()
            qr.save(buffer, format='PNG')
            buffer.seek(0)  # Reset the buffer position before saving
            file_name = f'{self.batch_qr_code_string}.png'
            self.batch_qr_code.save(file_name, File(buffer), save=False)

        super().save(*args, **kwargs)

    
    def latest_distributor(self):
        last_distribution = self.batchdistribution_set.last()
        if last_distribution and last_distribution.distributor:
            return last_distribution.distributor.username
        else:
            return "None"
    
        
    def latest_pharmacy(self):
        last_pharmacy = self.pharmacydistribution_set.last()
        if last_pharmacy and last_pharmacy.pharmacy:
            return last_pharmacy.pharmacy.username
        else:
            return "None"
        
    def is_sub_batch(self):
        return self.parent_batch is not None

    # inside your Batch model
    def create_sub_batch(self, quantity_to_be_sent):
        sub_batch = Batch.objects.create(
            batch_id=f"{self.batch_id}-D{self.sub_batches.count() + 1}", 
            drug_name=self.drug_name,
            manufacturer = self.manufacturer,
            drug_category = self.drug_category,
            quantity=quantity_to_be_sent,
            quantity_left=quantity_to_be_sent,
            manufacture_date=self.manufacture_date,  # required field
            parent_batch=self,
            expiry_date=self.expiry_date,
        )
        sub_batch.save()
        
        self.quantity_left -= quantity_to_be_sent
        self.save()
        return sub_batch  

          


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
    verified = models.BooleanField(default=False)




    def __str__(self):
        return f"{self.quantity_sent} units of {self.batch.drug_name} to {self.distributor.username}"
