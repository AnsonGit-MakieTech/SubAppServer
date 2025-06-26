import random

def get_product_showcase():
    recommended = {
        "1" : {
            "name": "Home Plan 1",
            "description": "This is the description of the product 1",
            "monthly" : 10000,
            "monthly_text" : "P10,000 / month",
            "speed" : 100,
            "speed_text" : "100 Mbps",
            "additional_text" : [ "Free-Setup:" "Professional Installation" ], 
        },
        "2" : {
            "name": "Home Plan 2",
            "description": "This is the description of the product 1",
            "monthly" : 10000,
            "monthly_text" : "P10,000 / month",
            "speed" : 100,
            "speed_text" : "100 Mbps",
            "additional_text" : [ "Free-Setup:" "Professional Installation" ], 
        } 
    }

    bussiness = {
        "3" : {
            "name": "Business Plan 1",
            "description": "This is the description of the product 1",
            "rate" : 10000,
            "rate_text" : "P10,000 / month",
            "speed" : 100,
            "speed_text" : "100 Mbps",
            "additional_text" : [ "Free-Setup:" "Professional Installation" ],
        },
        "4" : {
            "name": "Business Plan 2",
            "description": "This is the description of the product 1",
            "rate" :  10000,
            "rate_text" : "P10,000 / month",
            "speed" : 100,
            "speed_text" : "100 Mbps",
            "additional_text" : [ "Free-Setup:" "Professional Installation" ],
        }

    }

    return [
        {
            "title": "Recommended for you",
            "products": recommended
        },
        {
            "title": "Business Plan",
            "products": bussiness
        }
    ]



def register_account(data):
    """
    API for registrations for new installation of the app
    POST:
        data = {
            'is_applying': boolean,  # if true means the user is applying for a plan and if false means the user is just creating an account
            'plan_id': int | None, # the id of the plan the user is applying for
            'geolocation' : list[ latitude, longitude], # the geolocation of the user
            'fname': str, # the first name of the user
            'mname': str, # the middle name of the user
            'lname': str, # the last name of the user
            'email': str, # the email of the user
            'birthdate': str, # the birthdate of the user
            'street': str, # the street of the user
            'barangay': str, # the barangay of the user
            'address': str, # the address of the user
            'city': str, # the city of the user
            'primary_phone': str, # the primary phone of the user
            'secondary_phone': str, # the secondary phone of the user and its optional
            'third_phone': str, # the third phone of the user and its optional
            'valid_id' : str(file), # the valid id of the user which is a file converted to base64
            'username'': str, # the username of the user
            'password': str, # the password of the user
            'confirm_password': str, # the confirm password of the user
            'is_terms_and_conditions_accepted': boolean, # if true , then the user accepted to the terms and conditions
            'is_privacy_policy_accepted': boolean, # if true , then the user accepted to the privacy policy
            'is_pay_online': boolean, # if true means the user is paying online and if false means the user is paying on visit
            'is_pay_visit': boolean, # if true means the user is paying on visit and if false means the user is paying online 
        }
    """
    print("Processing registration...")
    for key, _ in data.items():
        print(f"Received : {key}")#

    if data.get("is_applying", False) and data.get("is_pay_online", False) and not data.get("is_pay_visit", False):
        print("User is paying online and new subscriber")
        return {
            'link' : 'https://alpha.billingko.com/'
        }
    elif data.get("is_applying", False) and not data.get("is_pay_online", False) and data.get("is_pay_visit", False):
        print("User is paying on visit and new subscriber")
        return {
            'appnum' : "AFDJ23"
        }
    elif data.get("is_applying", None) == False :
        print("User is an old subscriber and want to create an account")
        return True
    else:
        print("User is neither paying online nor on visit or old subscriber")
        return None


def forgot_password(data):
    """
    This function is used to handle the forgot password functionality.
    data = {
        'username' : str, # the username of the user
        'password' : str, # the password of the user
        'confirm_password' : str, # the confirm password of the user
    }
    """
    print("Processing forgot password...")
    for key, value in data.items():
        print(f"Received : {key} = {value}")
    print("Sending email to user...")
    return True



def get_cities():
    """
    This function is used to get the list of cities.
    """
    print("Getting cities...")
    return {
        '1' : 'City 1',
        '2' : 'City 2',
        '3' : 'City 3',
    }


def login_account(data):
    """
    This function is used to handle the login functionality.
    data = {
        'username' : str, # the username of the user
        'password' : str, # the password of the user
    }
    """
    print("Processing login...")
    for key, value in data.items():
        print(f"Received : {key} = {value}")
    return True


def get_account_info():
    """
    This function is used to get the account information.
    """
    print("Gettting account info...")
    return {
        'name' : "Argel Moronia Nava",
        'accountnum' : "10638899",
        'email' : "Helloworld@gmail.com",
        'type' : "Regular",
        'street' : "Purok 23",
        'barangay' : "Ibingay Boulevards",
        'city' : "Masbate City",
        'phone' : "09458935530"
    }



def get_wallet():
    """
    This function is used to get the wallet information.
    """
    print("Getting wallet info...")
    return {
        'unpaid' : 1000,
        'wallet' : 5000,
    }


def get_tickets():
    """
    This function is used to get the tickets information.
    """
    print("Getting filed tickets...")
    ticket = {
        'ticketnum' : '1234213',
        'ticketstatus' : 'open',
        'type' : 'repair' 
    }

    return {
        '1' : ticket,
        '2' : ticket,
        '3' : ticket
    }


def get_plans():
    """
    This function is used to get the plans information.
    """
    print("Getting subscriber plans...")
    plan = {
        'planname' : 'Basic 1',
        'monthly' : 1000,
        'status' : 'Registering',
        'addons' : {
            '1' : {
                'name' : 'Home Plan Add Ons 1',
                'monthly' : 5000
            },
            '2' : {
                'name' : 'Home Plan Add Ons 2',
                'monthly' : 5000
            },
        },
        'installments' : {
            '1' : {
                'name' : 'Installment 1',
                'monthly' : 15000,
                'month_to_pay' : 12,
                'month_remaining' : 4,
                'total_amount' : 40000
            },
            '2' : {
                'name' : 'Installment 1',
                'monthly' : 15000,
                'month_to_pay' : 12,
                'month_remaining' : 4,
                'total_amount' : 40000
            },
        }
    }

    return {
        '1' : plan,
        '2' : plan,
        '3' : plan
    }


def logout_account():
    """
    This function is used to logout the account.
    """
    print("Logging out...")
    return True

    











