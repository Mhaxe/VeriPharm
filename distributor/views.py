# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.decorators import distributor_required  # optional role check
from django.shortcuts import redirect, get_object_or_404
from manufacturer.models import BatchDistribution,Drug,Batch
from django.http import JsonResponse



@login_required
@distributor_required  
def distributor_dashboard(request):
    distributions = BatchDistribution.objects.filter(distributor=request.user)
    context = {
        'distributions': distributions
    }
    return render(request, 'distributor/dashboard.html',context)

@login_required
def verify_distribution(request, distribution_id):
    distribution = get_object_or_404(BatchDistribution, id=distribution_id, distributor=request.user)
    distribution.verified = True
    distribution.save()
    return redirect('distributor:dashboard') 

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
            batch = Batch.objects.get(batch_qr_code=query)
            
            # Get the related distribution record for this batch and current distributor
            if request.user.is_authenticated and request.user.role == "distributor":
                try:
                    distribution = BatchDistribution.objects.get(batch=batch, distributor=request.user)
                    distribution.verified = True
                    distribution.save()
                    return redirect("distributor:dashboard")
                except BatchDistribution.DoesNotExist:
                    error = "No distribution record found for this batch and your account."
        except Batch.DoesNotExist:
            batch = None

        if not drug and not batch:
            error = "Invalid or unregistered QR code."

    


def scan_camera(request):
    return render(request, "distributor/scan_camera.html")



from .forms import PharmacyDistributionForm

@login_required
def pass_to_pharmacy(request):
    if request.method == 'POST':
        form = PharmacyDistributionForm(request.POST, distributor=request.user)
        if form.is_valid():
            form.save()
            print("valid form")
            return redirect('distributor:dashboard')  # or any other success view
        else:
            print(f"not valid,{form.errors}")
    else:
        form = PharmacyDistributionForm(distributor=request.user)

    return render(request, 'distributor/transfer_to_pharmacy.html', {'form': form})

def about(request):
    return render(request, 'distributor/about_page.html')


@login_required
def verify_qr_code(request):
    code = request.GET.get('code', '').strip()
    try:
        batch = Batch.objects.get(drugs__qr_code_string=code)  # or filter by batch QR if it's batch-wide
        distribution = BatchDistribution.objects.get(batch=batch, distributor=request.user)

        if distribution.verified:
            return JsonResponse({'message': 'Already verified.'})
        
        distribution.verified = True
        distribution.save()
        return JsonResponse({'message': f'Batch {batch.batch_id} verified successfully!'})

    except Batch.DoesNotExist:
        return JsonResponse({'message': 'Invalid QR code. Batch not found.'})
    except BatchDistribution.DoesNotExist:
        return JsonResponse({'message': 'You are not authorized to verify this batch.'})




