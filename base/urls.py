

from django.urls import path
from  .views import *

urlpatterns = [ 
    path('test_action', overall_action, name='test_action'),
]

    