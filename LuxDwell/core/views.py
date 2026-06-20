from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import Property, Booking, Profile
from .forms import AdminUserCreationForm, PropertyForm, LuxDwellRegisterForm
from .models import Property, Booking, Profile
from.import models
from django.db.models import Sum

# --- PUBLIC ---
def home(request):
    # Base queryset: only approved properties
    properties = Property.objects.filter(is_approved=True)

    # Fetching all filter parameters from the URL
    query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    p_type = request.GET.get('type')

    # 1. Location Filter
    if query:
        properties = properties.filter(location__icontains=query)
    
    # 2. Minimum Price Filter
    if min_price:
        properties = properties.filter(price__gte=min_price)
        
    # 3. Maximum Price Filter
    if max_price:
        properties = properties.filter(price__lte=max_price)
        
    # 4. Property Type Filter (e.g., Villa, Apartment, Penthouse)
    if p_type and p_type != "All":
        properties = properties.filter(property_type__icontains=p_type)

    return render(request, 'core/index.html', {'properties': properties.order_by('-id')})

def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == "POST":
        message = request.POST.get('message')
        app_date = request.POST.get('appointment_date')
        app_time = request.POST.get('appointment_time')
        
        Booking.objects.create(
            user=request.user,
            property=property,
            message=message,
            appointment_date=app_date,
            appointment_time=app_time
        )
        messages.success(request, "Your appointment request has been sent!")
        return redirect('user_dashboard')
    
    return render(request, 'core/property_detail.html', {'property': property})

# --- AUTH ---
def register_view(request):
    if request.method == 'POST':
        form = LuxDwellRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            role = form.cleaned_data['role']
            Profile.objects.create(user=user, phone=form.cleaned_data['phone_number'], role=role)
            login(request, user)
            return redirect('agent_dashboard' if role == 'agent' else 'user_dashboard')
    return render(request, 'core/register.html', {'form': LuxDwellRegisterForm()})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff: return redirect('custom_admin')
            profile, _ = Profile.objects.get_or_create(user=user)
            return redirect('agent_dashboard' if profile.role == 'agent' else 'user_dashboard')
    return render(request, 'core/login.html', {'form': AuthenticationForm()})

def logout_view(request):
    if request.method == 'POST': logout(request)
    return redirect('home')

# --- DASHBOARDS ---
@login_required
def user_dashboard(request):
    # 1. Get User's Own Data (Listings and Enquiries)
    my_listings = Property.objects.filter(owner=request.user).order_by('-id')
    my_bookings = Booking.objects.filter(user=request.user).order_by('-request_date')
    
    # 2. Base Marketplace Query: Approved properties NOT owned by this user
    all_properties = Property.objects.filter(is_approved=True).exclude(owner=request.user)
    
    # 3. Fetching all filter parameters from the URL (now unified to use 'q' instead of 'detected_loc')
    query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    p_type = request.GET.get('type')

    # 4. Apply Filters
    if query:
        all_properties = all_properties.filter(location__icontains=query)
        
    if min_price:
        all_properties = all_properties.filter(price__gte=min_price)
        
    if max_price:
        all_properties = all_properties.filter(price__lte=max_price)
        
    if p_type and p_type != "All":
        # Using iexact to ensure strict matching (e.g., "Villa" matches "Villa" exactly)
        all_properties = all_properties.filter(property_type__iexact=p_type)
    
    context = {
        'my_listings': my_listings,
        'my_bookings': my_bookings,
        'all_properties': all_properties.order_by('-id'),
    }
    return render(request, 'core/user_dashboard.html', context)


def home(request):
    # Base queryset: only approved properties
    properties = Property.objects.filter(is_approved=True)

    # Fetching all filter parameters from the URL
    query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    p_type = request.GET.get('type')

    # Apply Filters
    if query:
        properties = properties.filter(location__icontains=query)
        
    if min_price:
        properties = properties.filter(price__gte=min_price)
        
    if max_price:
        properties = properties.filter(price__lte=max_price)
        
    if p_type and p_type != "All":
        # Using iexact to ensure strict matching
        properties = properties.filter(property_type__iexact=p_type)

    return render(request, 'core/index.html', {'properties': properties.order_by('-id')})

@login_required
def agent_dashboard(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if profile.role != 'agent':
        return redirect('user_dashboard')

    # IMPORTANT: Filter properties where the user is the assigned agent
    properties = Property.objects.filter(agent=request.user).order_by('-id')
    # Filter inquiries for those properties
    inquiries = Booking.objects.filter(property__agent=request.user).order_by('-request_date')

    context = {
        'properties': properties,
        'inquiries': inquiries,
    }
    return render(request, 'core/agent_dashboard.html', context)

@login_required
def agent_delete_inquiry(request, booking_id):
    # Security: Ensure the inquiry belongs to a property owned by the current agent
    inquiry = get_object_or_404(Booking, id=booking_id, property__owner=request.user)
    
    inquiry.delete()
    return redirect('agent_dashboard')


# --- ACTIONS ---
@login_required
def add_property(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.owner = request.user
            if profile.role == 'agent':
                prop.agent = request.user
                prop.is_approved = True # Auto-approve agents
            prop.save()
            form.save_m2m()
            return redirect('agent_dashboard' if profile.role == 'agent' else 'user_dashboard')
    return render(request, 'core/add_property.html', {'form': PropertyForm()})

@login_required
def book_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        Booking.objects.create(user=request.user, property=property_obj, message=request.POST.get('message'))
        return redirect('user_dashboard')
    return render(request, 'core/book.html', {'property': property_obj})

@login_required
def respond_to_inquiry(request, booking_id):  # Changed from inquiry_id to booking_id
    if request.method == "POST":
        inquiry = get_object_or_404(Booking, id=booking_id)
        
        # Get the status from the form
        new_status = request.POST.get('response_status')
        agent_reply = request.POST.get('agent_response')
        prop_status = request.POST.get('status_update')

        # Update and Save Booking
        inquiry.response_status = new_status
        inquiry.agent_response = agent_reply
        inquiry.is_resolved = True
        inquiry.save()

        # Update and Save Property Status
        property_obj = inquiry.property
        property_obj.status = prop_status
        property_obj.save()

        return redirect('agent_dashboard')

# --- ADMIN ---
def custom_admin(request):
    # 1. Fetch the statistics
    total_users = User.objects.count()
    agents_count = User.objects.filter(profile__role='agent').count()
    total_listings = Property.objects.count()
    
    # 2. Fetch the data for the tables
    pending_properties = Property.objects.filter(is_approved=False)
    all_properties = Property.objects.all()
    recent_users = User.objects.all().order_by('-date_joined')[:10] # Show last 10
    
    # 3. Pass EVERYTHING into the context
    context = {
        'total_users': total_users,
        'agents_count': agents_count,
        'total_listings': total_listings,
        'pending_properties': pending_properties,
        'all_properties': all_properties,
        'recent_users': recent_users,
    }
    
    return render(request, 'core/admin_portal.html', context)
@staff_member_required
def admin_add_user(request):
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('custom_admin')
    return render(request, 'core/admin_add_user.html', {'form': AdminUserCreationForm()})

@staff_member_required
def admin_edit_property(request, property_id):
    prop = get_object_or_404(Property, id=property_id)
    form = PropertyForm(request.POST or None, request.FILES or None, instance=prop)
    if form.is_valid():
        form.save()
        return redirect('custom_admin')
    return render(request, 'core/edit_property.html', {'form': form, 'property': prop})

@staff_member_required
def approve_property(request, property_id):
    prop = get_object_or_404(Property, id=property_id)
    prop.is_approved = True
    prop.save()
    return redirect('custom_admin')

@staff_member_required
def reject_property(request, property_id):
    prop = get_object_or_404(Property, id=property_id)
    prop.is_approved = False
    prop.save()
    return redirect('custom_admin')

@staff_member_required
def delete_property(request, property_id):
    Property.objects.get(id=property_id).delete()
    return redirect('custom_admin')

@staff_member_required
def delete_user(request, user_id):
    User.objects.get(id=user_id).delete()
    return redirect('custom_admin')

@login_required
def delete_booking(request, booking_id):
    # Security: Ensure the user can only delete their own bookings
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Optional: You might want to prevent deleting 'Accepted' bookings 
    # until the appointment date has passed.
    booking.delete()
    return redirect('user_dashboard')


@staff_member_required
def cancel_booking(request, booking_id):
    Booking.objects.get(id=booking_id).delete()
    return redirect('custom_admin')

@staff_member_required
def toggle_agent_status(request, user_id):
    p, _ = Profile.objects.get_or_create(user_id=user_id)
    p.role = 'agent' if p.role != 'agent' else 'user'
    p.save()
    return redirect('custom_admin')

@login_required
def toggle_property_status(request, prop_id):
    if request.method == "POST":
        property_obj = get_object_or_404(Property, id=prop_id, owner=request.user)
        new_status = request.POST.get('new_status')
        
        if new_status in ['Available', 'Sold', 'Rented', 'Reserved']:
            property_obj.status = new_status
            property_obj.save()
            
    return redirect('agent_dashboard')


@login_required
def handle_appointment(request, booking_id, action):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Ensure only the property owner/agent can respond
    if booking.property.owner != request.user:
        return redirect('home')

    if action == 'accept':
        booking.status = 'Accepted'
        booking.agent_response = "Your appointment has been confirmed. See you then!"
    elif action == 'reject':
        booking.status = 'Rejected'
        booking.agent_response = "Sorry, this slot is unavailable. Please choose another time."
    
    booking.save()
    return redirect('agent_dashboard')