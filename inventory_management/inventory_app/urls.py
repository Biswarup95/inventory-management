from django.urls import path, reverse_lazy
from . import views
from .views import InventoryListCreateView, InventoryRetrieveUpdateDeleteView

from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.home, name='home'),
    #following line is for directly loading login page
    # path('', RedirectView.as_view(url=reverse_lazy('user_login'))),
    path('login/', views.user_login, name='user_login'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='user_logout'),
    path('add_inventory_record/', views.add_inventory_record, name='add_inventory_record'),
    path('fetch_inventory/', views.fetch_inventory, name='fetch_inventory'),
    path('approve_inventory_record/', views.approve_inventory_record, name='approve_inventory_record'),
    path('inventory/', InventoryListCreateView.as_view(), name='inventory-list-create'),
    path('inventory/<int:pk>/', InventoryRetrieveUpdateDeleteView.as_view(), name='inventory-retrieve-update-delete'),
]
