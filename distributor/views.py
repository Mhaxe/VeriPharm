# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.decorators import distributor_required  # optional role check
from django.shortcuts import redirect, get_object_or_404
from manufacturer.models import BatchDistribution

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
    return redirect('dashboard')  


