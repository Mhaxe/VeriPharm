from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import manufacturer_required 
from accounts.views import logout
from .forms import *
from distributor.models import PharmacyDistribution


@login_required
@manufacturer_required  
#def manufacturer_dashboard(request):
 #   if request.method == 'POST' and 'logout_button' in request.POST:
  #      print("logout")
   #     logout(request)
    #    return redirect('home')
    #return render(request, 'manufacturer/dashboard.html')


def manufacturer_dashboard(request):
    batch_form = BatchForm()
    drug_form = DrugForm()
    distributor_form = BatchDistributionForm()

    if request.method == 'POST':
        batch_form = BatchForm(request.POST)
        drug_form = DrugForm(request.POST)
        distributor_form = BatchDistributionForm(request.POST)
        if batch_form.is_valid():
            batch = batch_form.save(commit=False)
            batch.manufacturer = request.user  
            batch.save()
            quantity = batch_form.cleaned_data['quantity']
            from .utils import generate_qr_code
            for _ in range(quantity):
                unique_qr_string = generate_qr_code()  # you define this in utils.py
                drug = Drug(
                    name=batch.drug_name,
                    batch=batch,
                    qr_code_string=unique_qr_string,
                )
                drug.save()  # This will auto-generate the QR image in .save()
                print(f'{quantity} drugs added successfully.')
        
        if drug_form.is_valid():
            drug_form.save()
        if distributor_form.is_valid():
            distribution = distributor_form.save(commit=False)  # Don't save yet
            batch = distribution.batch  # Get the related batch
        if distribution.quantity_sent <= batch.quantity_left:
            batch.quantity_left -= distribution.quantity_sent  # Subtract sent quantity
            batch.save()  # Save the updated batch
            distribution.save()  # Now save the distribution record
        else:
            # Handle the case where sent quantity is more than available
            print(request, "Cannot send more than available quantity.")
   


    return render(request, 'manufacturer/dashboard2.html', {
        'batch_form': batch_form,
        'drug_form': drug_form,
        'distributor_form': distributor_form,
    })


def about(request):
    return render(request,"manufacturer/about.html")


def scan(request):
    query = request.GET.get("code")
    drug = None
    error = None

    if query:
        try:
            drug = Drug.objects.get(qr_code_string=query)
        except Drug.DoesNotExist:
            error = "Invalid or unregistered QR code."

    return render(request, "manufacturer/scan.html", {"drug": drug, "error": error}) 

def scan_camera(request):
    return render(request, "manufacturer/scan_camera.html")


def manufacturer_records(request):
    batches = Batch.objects.filter(manufacturer=request.user).order_by('-manufacture_date')
    records = []

    for batch in batches:
        status = {
            'batch': batch,
            'sent_to_distributor': False,
            'sent_to_pharmacy': False,
            'distributor_verified': False,
            'pharmacy_verified': False,
        }

        # Check if batch was sent to distributor
        dist = BatchDistribution.objects.filter(batch=batch).first()
        if dist:
            status['sent_to_distributor'] = True
            status['distributor_verified'] = getattr(dist, 'verified', False)

            # Check if it reached pharmacy
            pharmacy_dist = PharmacyDistribution.objects.filter(batch=batch).first()
            if pharmacy_dist:
                status['sent_to_pharmacy'] = True
                status['pharmacy_verified'] = getattr(pharmacy_dist, 'verified', False)

        records.append(status)


    context = {"batches" : batches,
               "records" : records,}
    return render(request,"manufacturer/records.html",context=context)

