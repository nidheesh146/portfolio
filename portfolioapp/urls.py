from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.index_view,name='index_view'),
    path('contact/', views.contact_view, name='contact'),

]
