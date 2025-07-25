

from django.urls import path
from  .views import overall_action

urlpatterns = [ 
    path('test_action/', overall_action, name='test_action'), 
]

    