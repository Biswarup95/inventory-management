from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Inventory, UserRole, UserRecord

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import generics
from .serializers import InventorySerializer

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            # Return user details or token if using token authentication
            return Response({'message': 'Login successful', 'user': username})
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class InventoryListCreateView(generics.ListCreateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

class InventoryRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['signup_username']
        email = request.POST['email']
        password = request.POST['signup_password']
        confirm_password = request.POST['confirm_password']
        role = request.POST['user_role']

        # Check if passwords match
        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
        
        user = User.objects.create_user(username=username, email=email, password=password)

        user_record = UserRecord.objects.create(username=username, email=email, password=password)
        
        UserRole.objects.create(user=user, role=role)
        # Optionally, you can log in the user immediately after signup
        # login(request, user)

        # Redirect to login page after successful signup
        return redirect('user_login')
    else:
        return render(request, 'signup.html')

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
            #return JsonResponse({'message': 'Login successful'})
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
            #return JsonResponse({'error': 'Invalid credentials'}, status=400)
    else:
        return render(request, 'login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('user_login')


@login_required
@csrf_exempt
def add_inventory(request):
    if request.method == 'POST':
        user_role = UserRole.objects.filter(user=request.user).first()
        if user_role.role == 'Store Manager':
            # Store Managers can add inventory without approval
            return add_inventory_record(request)
        elif user_role.role == 'Department Manager':
            # Department Managers need approval from Store Manager
            return JsonResponse({'error': 'Department Managers require approval from Store Manager'}, status=403)
        else:
            return JsonResponse({'error': 'Permission denied'}, status=403)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
@csrf_exempt
def add_inventory_record(request):
    if request.method == 'POST':
        # Extract data from request
        # Create Inventory object with status='Pending' and approved=False
        inventory = Inventory.objects.create(
            product_id=request.POST['product_id'],
            product_name=request.POST['product_name'],
            vendor=request.POST['vendor'],
            mrp=request.POST['mrp'],
            batch_num=request.POST['batch_num'],
            batch_date=request.POST['batch_date'],
            quantity=request.POST['quantity'],
            status='Pending',
            approved=False
        )
        return JsonResponse({'message': 'Inventory record added successfully'})
    else:
        return render(request, 'add_inventory.html')
        #return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
@csrf_exempt
def fetch_inventory(request):
    if request.method == 'GET':
        user_role = UserRole.objects.filter(user=request.user).first()
        if user_role.role == 'Store Manager':
            # Store Managers can fetch all pending inventory items
            pending_inventory = Inventory.objects.filter(status='Pending').values()
            return JsonResponse({'inventory': list(pending_inventory)})
        elif user_role.role == 'Department Manager':
            return JsonResponse({'error': 'Department Managers cannot fetch pending inventory'}, status=403)
        else:
            return JsonResponse({'error': 'Permission denied'}, status=403)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
@csrf_exempt
def approve_inventory(request):
    if request.method == 'POST':
        user_role = UserRole.objects.filter(user=request.user).first()
        if user_role.role == 'Store Manager':
            # Store Managers can approve pending inventory items
            return approve_inventory_record(request)
        elif user_role.role == 'Department Manager':
            return JsonResponse({'error': 'Department Managers cannot approve inventory'}, status=403)
        else:
            return JsonResponse({'error': 'Permission denied'}, status=403)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
@csrf_exempt
def approve_inventory_record(request):
    if request.method == 'POST':
        inventory_id = request.POST['inventory_id']
        try:
            inventory = Inventory.objects.get(id=inventory_id)
            inventory.status = 'Approved'
            inventory.approved = True
            inventory.save()
            return JsonResponse({'message': 'Inventory approved successfully'})
        except Inventory.DoesNotExist:
            return JsonResponse({'error': 'Inventory not found'}, status=404)
    else:
        return render(request, 'approve_inventory.html')
        #return JsonResponse({'error': 'Method not allowed'}, status=405)