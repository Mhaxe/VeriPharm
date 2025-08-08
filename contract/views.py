from django.shortcuts import render
from .models import BlockchainLog

def logs_view(request):
    actor = request.GET.get('actor')
    log_type = request.GET.get('log_type')

    logs = BlockchainLog.objects.all()

    if actor:
        logs = logs.filter(actor=actor)

    if log_type:
        logs = logs.filter(log_type=log_type)

    logs = logs.order_by('-block_number')  # Latest first

    return render(request, 'contract/logs.html', {
        'logs': logs,
        'selected_actor': actor,
        'selected_log_type': log_type,
    })
