from django.shortcuts import render
from .blockchain import contract, w3

def register_drug(request):
    if request.method == 'POST':
        batch_id = request.POST['batch_id']
        drug_name = request.POST['drug_name']
        manufacturer = request.POST['manufacturer']
        manufacture_date = int(request.POST['manufacture_date'])  # timestamp
        expiry_date = int(request.POST['expiry_date'])

        tx = contract.functions.registerDrug(
            batch_id, drug_name, manufacturer, manufacture_date, expiry_date
        ).build_transaction({
            'from': w3.eth.accounts[0],
            'gas': 3000000,
            'nonce': w3.eth.get_transaction_count(w3.eth.accounts[0])
        })

        signed_tx = w3.eth.account.sign_transaction(tx, private_key="0xYourPrivateKey")
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        w3.eth.wait_for_transaction_receipt(tx_hash)

        return render(request, 'contracts/success.html')

    return render(request, 'contracts/register.html')

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .blockchain import contract  # assumes you already imported the contract instance

@staff_member_required
def view_logs(request):
    logs = []

    try:
        event_filter = contract.events.Log.createFilter(from_block=0)
        events = event_filter.get_all_entries()

        for event in events:
            logs.append({
                'message': event['args']['message'],
                'timestamp': event['blockNumber']
            })

    except Exception as e:
        logs = [{'message': f'Error fetching logs: {str(e)}', 'timestamp': '-'}]

    return render(request, 'contracts/logs.html', {'logs': logs})

# blockchain/views.py
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .blockchain import get_contract_instance

@staff_member_required
def logs_view(request):
    contract = get_contract_instance()
    events = contract.events.LogMessage().get_logs(from_block=0)
    context = {
        "events": [
            {
                "message": e["args"]["message"],
                "block": e["blockNumber"]
            } for e in events
        ]
    }
    return render(request, "contract/logs.html", context)


