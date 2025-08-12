from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from manufacturer.models import Batch

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_batch(request, code):
    try:
        batch = Batch.objects.get(batch_qr_code_string=code)
        return Response({
            "valid": True,
            "message": f"{batch.drug_name} - {batch.batch_id} is authentic",
            "expiry_date": batch.expiry_date
        })
    except Batch.DoesNotExist:
        return Response({
            "valid": False,
            "message": "Drug batch not found or invalid."
        }, status=404)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from manufacturer.models import Batch  # Assuming QR codes are linked to your Batch model

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_qr_code(request):
    code = request.GET.get("code")
    if not code:
        return Response({"status": "error", "message": "QR code not provided"}, status=400)

    batch = Batch.objects.filter(batch_id=code).first()
    if batch:
        return Response({
            "status": "success",
            "batch_id": batch.batch_id,
            "drug_name": batch.drug_name,
            "manufacturer": batch.manufacturer.name if batch.manufacturer else None,
        })
    else:
        return Response({"status": "error", "message": "Invalid or unknown QR code"}, status=404)
