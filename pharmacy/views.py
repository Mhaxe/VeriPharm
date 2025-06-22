from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from distributor.models import PharmacyDistribution  
from accounts.decorators import pharmacy_required

@login_required
@pharmacy_required
def pharmacy_dashboard(request):
    received_batches = PharmacyDistribution.objects.filter(pharmacy=request.user)
    return render(request, 'pharmacy/dashboard.html', {'received_batches': received_batches})

@login_required
@pharmacy_required
def verify_receipt(request, distribution_id):
    distribution = get_object_or_404(PharmacyDistribution, id=distribution_id, pharmacy=request.user)
    distribution.verified = True
    distribution.save()
    return redirect('pharmacy:dashboard')
