# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.decorators import distributor_required  # optional role check
from django.shortcuts import redirect, get_object_or_404
from contract.blockchain import log_event
from manufacturer.models import BatchDistribution,Drug,Batch
from django.http import JsonResponse
from .models import PharmacyDistribution



@login_required
@distributor_required  
def distributor_dashboard(request):
    distributions = BatchDistribution.objects.filter(distributor=request.user).order_by('-distribution_date')
    pharmacy_map = {
        pd.batch.id: pd for pd in PharmacyDistribution.objects.filter(distributor=request.user).select_related('pharmacy')
    }


    context = {
        'distributions': distributions,
        'pharmacy_map': pharmacy_map,
    }
    return render(request, 'distributor/dashboard.html', context)

@login_required
def verify_distribution(request, distribution_id):
    distribution = get_object_or_404(BatchDistribution, id=distribution_id, distributor=request.user)
    distribution.verified = True
    distribution.save()
    log_event(f"Distributor:{request.user} verified Batch:{distribution.batch.batch_id} containing {distribution.batch.quantity_left} number of drugs from Manufacturer:{distribution.batch.manufacturer}",actor=request.user,log_type='verification')  
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
            print("trying batch")
            batch = Batch.objects.get(batch_qr_code_string=query)
            print(f"batch:{batch}")
            # Get the related distribution record for this batch and current distributor
            if request.user.is_authenticated and request.user.role == "distributor":
                try:
                    distribution = BatchDistribution.objects.get(batch=batch, distributor=request.user)
                    distribution.verified = True
                    distribution.save()
                    log_event(f"Distributor:{request.user} verified Batch:{distribution.batch.batch_id} containing {distribution.batch.quantity_left} number of drugs from Manufacturer:{distribution.batch.manufacturer}",actor=request.user,log_type='verification')
                    return redirect("distributor:dashboard")
                except BatchDistribution.DoesNotExist:
                    error = "No distribution record found for this batch and your account."
        except Batch.DoesNotExist:
            batch = None

        if not drug and not batch:
            error = "Invalid or unregistered QR code."

        print(error)
        print(query)
    return render(request, "distributor/scan.html", {"drug": drug, "error": error})  


    


def scan_camera(request):
    return render(request, "distributor/scan_camera.html")



from .forms import PharmacyDistributionForm

@login_required
def pass_to_pharmacy(request):
    error = ''
    if request.method == 'POST':
        form = PharmacyDistributionForm(request.POST, distributor=request.user)

        if form.is_valid():
            instance = form.save(commit=False)

            # Get the distributor's allocation from manufacturer
            distribution = BatchDistribution.objects.filter(
                batch=instance.batch,
                distributor=request.user,
                verified=True,
                finished=False
            ).first()

            if not distribution:
                error = "You have no active stock for this batch."
            elif instance.quantity_sent > distribution.quantity_sent:
                error = "Cannot send more than available quantity."
            elif instance.quantity_sent == distribution.quantity_sent:
                # Send all stock to pharmacy
                distribution.finished = True
                distribution.save()

                instance.save()  # PharmacyDistribution record
            else:
                # Send part of the stock
                #distribution.quantity_sent -= instance.quantity_sent
                sub_batch = distribution.create_sub_batch(instance.quantity_sent)
                distribution.save()
                instance.batch = sub_batch.batch
                instance.save()  # PharmacyDistribution record

            if not error:
                log_event(
                    f"Distributor:{request.user} sent {instance.quantity_sent} units of Batch:{instance.batch} to Pharmacy:{instance.pharmacy}",
                    actor=request.user,
                    log_type='verification'
                )
                return redirect('distributor:dashboard')

        else:
            print(f"Form invalid: {form.errors}")

    else:
        form = PharmacyDistributionForm(distributor=request.user)

    return render(request, 'distributor/transfer_to_pharmacy.html', {'form': form, 'error': error})


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




