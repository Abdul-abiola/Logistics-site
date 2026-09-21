from django.contrib import admin
from .models import User, Shipment, ShipmentEvent, Enquiry

# Register your models here.

admin.site.register(User)
admin.site.register(Shipment)
admin.site.register(ShipmentEvent)
admin.site.register(Enquiry)
