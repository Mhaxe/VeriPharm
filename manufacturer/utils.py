import uuid
from .models import Drug

def generate_qr_code():
    return uuid.uuid4().hex

def fill_qr_code():
    for drug in Drug.objects.all():
        if not drug.qr_code_string:
            drug.qr_code_string = generate_qr_code()
            drug.save()