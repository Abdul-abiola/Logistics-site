from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Shipment, ShipmentEvent, User, Enquiry
from .forms import ShipmentForm, ShipmentStatusForm, CustomerRegisterForm, EnquiryForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


# Create your views here.

# logistics = [
#     {'id': 1, 'Driver_name': 'Abdul', 'status': 'Delivered', 'Location': 'Lagos', 'Tracking_number': '1234567890'},
#     {'id': 2, 'Driver_name': 'Emeka', 'status': 'In Transit', 'Location': 'Abuja', 'Tracking_number': '0987654321'},
#     {'id': 3, 'Driver_name': 'Chioma', 'status': 'Pending', 'Location': 'Abia', 'Tracking_number': '4692254321'},
    
# ] 
# logistics = []


def loginPage(request):  
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')  
        else:
            messages.error(request, 'Invalid username or password ')
              
                
    context = {'page' : page}
    return render(request, 'logistics_site/login_register.html', context)

def registerPage(request):
    form = CustomerRegisterForm()   # ← must be this, not ShipmentForm

    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)   # ← same here
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'customer'
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'logistics_site/login_register.html', {'form': form})
    
def home(request):
    return render(request, 'logistics_site/home.html')

@login_required
def index(request):
    logistics = Shipment.objects.filter(customer=request.user)
    context = {'logistics': logistics}
    return render(request, 'logistics_site/index.html', context)


def logoutUser(request):
    logout(request)
    return redirect('index')


@login_required
def createShipment(request):
    form = ShipmentForm()
    
    if request.method == 'POST':
        form = ShipmentForm(request.POST)
        if form.is_valid():
            shipment = form.save(commit=False)
            shipment.customer = request.user
            shipment.save()
            
            ShipmentEvent.objects.create(
                shipment=shipment,
                status='pending',
                location='',
                note='Shipment created'
            )
            return redirect('shipment-detail', pk=shipment.id)

    return render(request, 'logistics_site/shipment_form.html', {'form': form})


@login_required
def shipmentDetail(request, pk):
    shipment = get_object_or_404(Shipment, id=pk)

    if (request.user != shipment.customer
            and request.user != shipment.driver
            and request.user.role != 'admin'):
        return HttpResponse("You are not allowed to view this shipment")

    events = shipment.events.all()
    return render(request, 'logistics_site/shipment_details.html',
                  {'shipment': shipment, 'events': events})

def updateShipmentStatus(request, pk):
    shipment = get_object_or_404(Shipment, id=pk)

    if request.user != shipment.driver and request.user.role != 'admin':
        return HttpResponse("You are not allowed to update this shipment")

    form = ShipmentStatusForm(initial={'status': shipment.status})

    if request.method == 'POST':
        form = ShipmentStatusForm(request.POST)
        if form.is_valid():
            new_status = form.cleaned_data['status']
            location = form.cleaned_data['location']
            note = form.cleaned_data['note']

            shipment.status = new_status
            shipment.location = location
            shipment.save()

            ShipmentEvent.objects.create(
                shipment=shipment,
                status=new_status,
                location=location,
                note=note
            )
            return redirect('shipment-detail', pk=shipment.id)

    return render(request, 'logistics_site/update-status.html', {'form': form, 'shipment': shipment})

@login_required
def trackByNumber(request):
    """Public page — no login needed, just type a tracking number."""
    shipment = None
    tracking_number = request.GET.get('tracking_number')

    if tracking_number:
        try:
            shipment = Shipment.objects.get(tracking_number=tracking_number)
        except Shipment.DoesNotExist:
            shipment = None

    context = {'shipment': shipment, 'tracking_number': tracking_number}
    return render(request, 'logistics_site/track.html', context)


@login_required
def cancelShipment(request, pk):
    shipment = get_object_or_404(Shipment, id=pk, customer=request.user)

    if shipment.status == 'pending':
        shipment.status = 'cancelled'
        shipment.save()

        ShipmentEvent.objects.create(
            shipment=shipment,
            status='cancelled',
            location='',
            note='Shipment cancelled by customer'
        )

    return redirect('shipment-detail', pk=shipment.id)

@login_required
def editShipment(request, pk):
    shipment = get_object_or_404(Shipment, id=pk, customer=request.user)

    if shipment.status != 'pending':
        return redirect('shipment-detail', pk=shipment.id)

    if request.method == 'POST':
        form = ShipmentForm(request.POST, instance=shipment)
        if form.is_valid():
            form.save()

            ShipmentEvent.objects.create(
                shipment=shipment,
                status=shipment.status,
                location='',
                note='Shipment details edited by customer'
            )
            return redirect('shipment-detail', pk=shipment.id)
    else:
        form = ShipmentForm(instance=shipment)

    return render(request, 'logistics_site/shipment_form.html', {'form': form})

@login_required
def myShipments(request):
    q = request.GET.get('q', '').strip()

    shipments = Shipment.objects.filter(customer=request.user)

    if q:
        shipments = shipments.filter(tracking_number__iexact=q)

    return render(request, 'logistics_site/my_shipments.html', {'shipments': shipments, 'q': q})

# @login_required
# def myShipments(request):
#     shipments = Shipment.objects.filter(customer=request.user)
#     return render(request, 'logistics_site/my_shipments.html', {'shipments': shipments})




@login_required
def driverDashboard(request):
    shipments = Shipment.objects.filter(driver=request.user)
    return render(request, 'logistics_site/driver_dashboard.html', {'shipments': shipments})

def service(request, pk): 
    return render(request, 'service.html')

def sendEnquiry(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Enquiry.objects.filter(email=email).exists():
                messages.error(request, "You've already submitted an enquiry with this email.")
                return redirect('home')

            form.save()
            messages.success(request, "Thanks! We'll get back to you shortly.")
            return redirect('home')
    else:
        form = EnquiryForm()

    return render(request, 'logistics_site/home.html', {'form': form})
    
