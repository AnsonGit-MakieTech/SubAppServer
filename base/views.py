from django.shortcuts import render
from django.http import JsonResponse
import json
# Create your views here.


def apply_intro(request):
    """
    API for registrations for new installation of the app
    POST:
        data = {
            'has_already_account': boolean,
            'plan_id': int,
            'geolocation' : list[ latitude, longitude],
            'fname': str,
            'mname': str,
            'lname': str,
            'email': str,
            'strreet': str,
            'barangay': str,
            'address': str,
            'city': str,
            'primary_phone': str,
            'secondary_phone': str,
            'third_phone': str,
            'valid_id' : str(file),
            'username'': str,
            'password': str,
            'confirm_password': str,
            'is_terms_and_conditions_accepted': boolean,
            'is_privacy_policy_accepted': boolean,
            'is_pay_online': boolean,
            'is_pay_visit': boolean,
        }
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        return JsonResponse({'status': 'success'})


