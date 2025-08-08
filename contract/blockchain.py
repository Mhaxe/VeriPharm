from .models import BlockchainLog
from django.utils import timezone
import uuid

def log_event(message: str,actor,log_type):
    BlockchainLog.objects.create(
        message=message,
        tx_hash=f"0x{uuid.uuid4().hex.ljust(64, '0')[:64]}",
        timestamp=timezone.now(),
        actor = actor,
        log_type = log_type,
    )
