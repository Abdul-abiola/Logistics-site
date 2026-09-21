from django.urls import path
from . import views
urlpatterns = [
    path('index/', views.index, name='index'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('cancel-shipment/<int:pk>/', views.cancelShipment, name='cancel-shipment'),
    path('', views.home, name='home'),
    path('create-shipment/', views.createShipment, name='create-shipment'),
    path('driver-dashboard/', views.driverDashboard, name='driver-dashboard'),
    path('edit-shipment/<int:pk>/', views.editShipment, name='edit-shipment'),
    path('shipment-details/<int:pk>/', views.shipmentDetail, name='shipment-detail'),
    # path('service/', views.service,  name='service'), 
    path('my-shipments/', views.myShipments, name='my-shipments'),
    path('update-shipment-status/<int:pk>/', views.updateShipmentStatus,name='update-shipment-status'),
    path('track/', views.trackByNumber, name='track-shipment'),
    path('send-enquiry/', views.sendEnquiry, name='send-enquiry'),
]
