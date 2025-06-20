

from django.urls import path
from  .views import *

urlpatterns = [ 
    path('apply_intro', apply_intro, name='apply_intro'),
]

