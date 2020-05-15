from django.shortcuts import render,redirect
from .models import Product,Customer,Order
from django.forms import inlineformset_factory
from .forms import OrderForm
from .filters import OrderFilter
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from .forms import OrderUserForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


@login_required(login_url="login")
def home(request):
    customer = Customer.objects.all()
    order = Order.objects.all()
    total_order = order.count()
    order_deivered = Order.objects.filter(status="Delivered").count()
    orders_pending = Order.objects.filter(status="Pending").count()
    return render(request,'accounts/index.html',{'customer':customer,'order':order,'total_order':total_order,'order_deivered':order_deivered,'orders_pending':orders_pending})

def product(request):
    product = Product.objects.all()
    return render(request,'accounts/products.html',{'product':product})

def orders(request):
    return render(request,'accounts/orders.html')

def customer(request,id):
    customer = Customer.objects.get(id=id)
    order = customer.order_set.all()
    total_order = order.count()

    # myFilter = OrderFilter(request.GET,queryset=order)
    # order = myFilter.qs

    context = {'customer':customer,'order':order,'total_order':total_order}
    return render(request,'accounts/customer.html',context)

def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=3)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.POST:
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid:
            formset.save()
            return redirect('/')


    context = {'formset':formset}
    return render(request,'accounts/form.html',context)

def updateForm(request,pk):
    order = Order.objects.get(id=pk)
    # print(order)
    form = OrderForm(instance=order)
    # print(form)
    if request.POST:
        form = OrderForm(request.POST,instance=order)
        if form.is_valid:
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request,'accounts/form.html',context)

def delete_form(request,pk):
    order = Order.objects.get(id=pk)
    if request.POST:
        order.delete()
        return redirect('/')
    context = {'order':order}

    return render(request,'accounts/deleteForm.html',context)

def OrderFilter(request):
    return render(request)

def loginview(request):
    if request.user.is_authenticated:
        return redirect('Dashboard')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('Dashboard')
        else:
            messages.info(request,"Incorrect Username or Password")

    context = {}
    return render(request,'accounts/login.html',context)

def UserPage(request):
    context = {}
    return render(request,'accounts/user.html',context)

def logoutuser(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('Dashboard')
    else:
        form = OrderUserForm()
        if request.method =='POST':
            form = OrderUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data['username']
                messages.success(request,"Signup successful for " +user )
                return redirect('login')
        context = {'form':form}
        return render(request,'accounts/register.html',context)
# Create your views here.
