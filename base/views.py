from django.shortcuts import render
from django.http import JsonResponse
import json
from .actions_path import *
# Create your views here.

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def overall_action(request):

    if request.method == 'POST':
        return_data = None
        data = json.loads(request.body)
        # print(data)
        if data.get('action') == 'get_product_showcase':
            return_data = get_product_showcase()
         
        if data.get('action') == 'register_account':
            return_data = register_account(data)

        if data.get('action') == 'forgot_password':
            return_data = forgot_password(data)
        
        
        if data.get('action') == 'get_cities':
            return_data = get_cities()
        
        
        if data.get('action') == 'login_account':
            return_data = login_account(data)

        
        if data.get('action') == 'get_account_info':
            return_data = get_account_info()


        
        if data.get('action') == 'get_cities':
            return_data = get_cities()


        
        if data.get('action') == 'get_wallet':
            return_data = get_wallet()


        
        if data.get('action') == 'get_tickets':
            return_data = get_tickets()


        
        if data.get('action') == 'get_plans':
            return_data = get_plans()


        
        if data.get('action') == 'logout_account':
            return_data = logout_account()
        


        
        if data.get('action') == 'add_ticket':
            return_data = add_ticket(data)
        




        return JsonResponse({'text': 'success', 'data': return_data})
    
    return JsonResponse({'text': 'error'})




