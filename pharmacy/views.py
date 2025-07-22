from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from distributor.models import PharmacyDistribution  
from accounts.decorators import pharmacy_required
from manufacturer.models import Drug,Batch


@login_required
@pharmacy_required
def pharmacy_dashboard(request):
    user = request.user.username 
    if user:
        print(user)
    received_batches = PharmacyDistribution.objects.filter(pharmacy=request.user)
    context = {
        'received_batches': received_batches,
        'current_user' : user,

    }
    return render(request, 'pharmacy/dashboard.html',context)

@login_required
@pharmacy_required
def verify_receipt(request, distribution_id):
    distribution = get_object_or_404(PharmacyDistribution, id=distribution_id, pharmacy=request.user)
    distribution.verified = True
    distribution.save()
    return redirect('pharmacy:dashboard')

def scan(request):
    query = request.GET.get("code")
    drug = None
    error = None

    if query:
        try:
            drug = Drug.objects.get(qr_code_string=query)
            return render(request, "distributor/scan.html", {"drug": drug, "error": error})
        except Drug.DoesNotExist:
            drug = None

        try:
            print("trying batch")
            batch = Batch.objects.get(batch_qr_code_string=query)
            print(f"batch:{batch}")
            # Get the related distribution record for this batch and current pharmacy
            if request.user.is_authenticated and request.user.role == "pharmacist":
                try:
                    pharmacy_distribution = PharmacyDistribution.objects.get(batch=batch, pharmacy=request.user)
                    pharmacy_distribution.verified = True
                    pharmacy_distribution.save()
                    return redirect("pharmacy:dashboard")
                except PharmacyDistribution.DoesNotExist:
                    error = "No distribution record found for this batch and your account."
        except Batch.DoesNotExist:
            batch = None

        if not drug and not batch:
            error = "Invalid or unregistered QR code."

        print(error)
        print(query)
    return render(request, "pharmacy/scan.html", {"drug": drug, "error": error})

def scan_camera(request):
    return render(request, "pharmacy/scan_camera.html")