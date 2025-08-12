from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import manufacturer_required 
from accounts.views import logout
from .forms import *
from distributor.models import PharmacyDistribution
from contract.blockchain import log_event

from django.http import FileResponse, Http404
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
    batch_form_error = ''
    distributor_form_error=''
    code_form_error = ''
    code_form = CodeForm()

    if request.method == 'POST':
        print("post req made")
        batch_form = BatchForm(request.POST)
        drug_form = DrugForm(request.POST)
        distributor_form = BatchDistributionForm(request.POST)
        code_form = CodeForm(request.POST)
        
    
        if batch_form.is_valid():
            manufacture_date = batch_form.cleaned_data['manufacture_date']
            expiry_date = batch_form.cleaned_data['expiry_date']

            # Check that expiry is not before manufacture
            if expiry_date < manufacture_date:
                print("exp_date<man_date")
                batch_form_error ='Expiry date cannot be earlier than manufacture date.'
            else:
                print("valid date")
                batch = batch_form.save(commit=False)
                batch.manufacturer = request.user  
                batch.save()

                quantity = batch_form.cleaned_data['quantity']
                from .utils import generate_qr_code

                for _ in range(quantity):
                    unique_qr_string = generate_qr_code()
                    drug = Drug(
                        name=batch.drug_name,
                        batch=batch,
                        qr_code_string=unique_qr_string,
                    )
                    drug.save()
                
                log_event(f"Manufacturer:{request.user} created Batch:{batch.batch_id} containing {quantity} number of drugs",actor='manufacturer',log_type='creation')
                print(f'{quantity} drugs added successfully.')

        
            
        if drug_form.is_valid():
            instance = drug_form
            log_event(f"Manufacturer:{request.user} created Drug:{instance.name} to batch{instance.batch}",
                      actor='manufacturer',
                      log_type='creation')
            drug_form.save()

        if distributor_form.is_valid():
            distribution = distributor_form.save(commit=False)
            original_batch = distribution.batch
            if distribution.quantity_sent < original_batch.quantity_left and original_batch.finished == False:
                sub_batch = original_batch.create_sub_batch(distribution.quantity_sent)
                distribution.batch = sub_batch
                distribution.save()
                print(f"sent {distribution.quantity_sent}")
                log_event(f"Manufacturer:{request.user} transfered Batch:{sub_batch.batch_id} containing {distribution.quantity_sent} number of drugs to Distributor:{distribution.distributor}",actor=request.user,log_type='transfer')  
            elif distribution.quantity_sent == original_batch.quantity_left and original_batch.finished == False:
                # Send the whole batch without creating a sub-batch
                distribution.batch = original_batch
                #original_batch.quantity_left = 0
                original_batch.finished = True
                original_batch.save()
                distribution.save()
                print(f"Sent entire batch ({distribution.quantity_sent} drugs)")
                log_event(
                    f"Manufacturer:{request.user} transferred ENTIRE Batch:{original_batch.batch_id} containing {distribution.quantity_sent} drugs to Distributor:{distribution.distributor}",
                    actor='distributor',
                    log_type='transfer'
                )
            else:
                print("Cannot send more than available quantity.")
                distributor_form_error = "Cannot send more than available quantity."


        if code_form.is_valid():
            try:
                print("valid code form")
                instance = code_form.save(commit=False)
                _batch_id = instance.batch_id
                print(_batch_id)
                batch = Batch.objects.filter(id=_batch_id).first()
                print(batch)
                if batch and batch.batch_qr_code:
                    return FileResponse(batch.batch_qr_code.open('rb'), as_attachment=True, filename=batch.batch_qr_code.name.split('/')[-1])
                else:
                    code_form_error = "QR code image not found"
            except(ValueError):
                pass        

            



    return render(request, 'manufacturer/dashboard2.html', {
        'batch_form': batch_form,
        'drug_form': drug_form,
        'distributor_form': distributor_form,
        'batch_form_error': batch_form_error,
        'distributor_form_error':distributor_form_error,
        'code_form_error':code_form_error
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


    context = {"records" : records,}
    return render(request,"manufacturer/records.html",context=context)

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
        except Batch.DoesNotExist:
            batch = None

        if not drug and not batch:
            error = "Invalid or unregistered QR code."

        print(error)
        print(query)
    return render(request, "manufacturer/scan.html", {"drug": drug, "error": error,"batch":batch})  



