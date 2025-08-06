from django.db import models
from django.utils import timezone

class BlockchainLog(models.Model):
    ACTOR_CHOICES = [
        ('manufacturer', 'Manufacturer'),
        ('distributor', 'Distributor'),
        ('pharmacy', 'Pharmacy'),
        ('admin', 'Admin'),
    ]

    LOG_TYPE_CHOICES = [
        ('creation', 'Batch Creation'),
        ('transfer', 'Drug Transfer'),
        ('verification', 'Verification'),
        ('general', 'General'),
    ]

    message = models.TextField()
    block_number = models.IntegerField(blank=True)
    tx_hash = models.CharField(max_length=66, unique=True)
    timestamp = models.DateTimeField(default=timezone.now)
    actor = models.CharField(max_length=20, choices=ACTOR_CHOICES, default='admin')
    log_type = models.CharField(max_length=20, choices=LOG_TYPE_CHOICES, default='general')

    def save(self, *args, **kwargs):
        if not self.block_number:
            latest_block = BlockchainLog.objects.order_by('-block_number').first()
            self.block_number = (latest_block.block_number + 1) if latest_block else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.message} (Block {self.block_number})"
