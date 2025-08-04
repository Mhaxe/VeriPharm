from django.db import models

# Create your models here.
class BlockchainLog(models.Model):
    message = models.TextField()
    block_number = models.IntegerField()
    tx_hash = models.CharField(max_length=66, unique=True)  # 66 for 0x + 64 hex chars
    timestamp = models.DateTimeField()
    
    def __str__(self):
        return f"{self.message} (Block {self.block_number})"