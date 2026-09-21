from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Shipment, User, Enquiry

class CustomerRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
        
class ShipmentStatusForm(forms.Form):
    status = forms.ChoiceField(choices=Shipment.STATUS_CHOICES)
    location = forms.CharField(max_length=200, required=False)
    note = forms.CharField(widget=forms.Textarea, required=False)
    
    
class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['sender_name', 'sender_address','sender_phone', 'recipient_name',
                  'recipient_address', 'recipient_phone', 'weight_kg',
                  'estimated_delivery']  
        
class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['company', 'email', 'pickup_state', 'cargo_description']        
           