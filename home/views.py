from django.shortcuts import render,redirect
from django.contrib.auth.models import User,AnonymousUser
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from .forms import ProfileForm
from .models import Address, Contact, Order, Pizza, Profile
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    try:
        if request.user.is_authenticated:
            if request.user and request.user != AnonymousUser:
                
                current_user = request.user
                ordersOfCurrentuser = Order.objects.filter(user = current_user)
                totalOrderList = []

                for pizzaOrder in ordersOfCurrentuser:
                    quantity = pizzaOrder.quantity
                    totalOrderList.append(quantity)

                totalOrders = sum(totalOrderList)
            else:
                totalOrders = 0
            context = {'totalOrders':totalOrders}
        return render(request,'home/index.html',context)
    except:
        
        return render(request,'home/index.html') 


def orders(request):
    try:
        if request.user:
            current_username = request.user.username
            
            user = User.objects.filter(username = current_username).first()
            orders = Order.objects.filter(user=user)
            price_list = []
            for order in orders:
                price_list.append(order.pizza_price)
            totalprice = round(sum(price_list),3) 
            if request.user and request.user != AnonymousUser:
            
                current_user = request.user
                ordersOfCurrentuser = Order.objects.filter(user = current_user)
                totalOrderList = []

                for pizzaOrder in ordersOfCurrentuser:
                    quantity = pizzaOrder.quantity
                    totalOrderList.append(quantity)

                totalOrders = sum(totalOrderList)
            else:
                totalOrders = 0
            ordersOfCurrentuser = Order.objects.filter(user = request.user)
                
            firstobjectofCurrentuser = ordersOfCurrentuser.first() 
            context = {
                'orders':orders,
                'totalOrders':totalOrders,
                'totalprice':totalprice,
                'firstobjectofCurrentuser':firstobjectofCurrentuser
                }
            return render(request,'home/orders.html',context)
    except Exception:
        messages.warning(request,'Please login to continue !')
        return redirect('login_data')
    

def increament(request):
    if request.method == 'POST':
        if 'order_id' in request.POST:
            pizzaname = request.POST['pizza_name']
            order_id = request.POST['order_id']
            order = Order.objects.filter(id=order_id)
            order_inst = order.first()
            pizzaprice = Pizza.objects.filter(pizza_name = pizzaname).first().pizza_price
            if order_inst.quantity == 0:
                
                order_inst.quantity = 1
                order_inst.save()
                return redirect('orders')
            else:
                
                order_quantity = order_inst.quantity
                order_quantity += 1
                order_inst.quantity = order_quantity
                order_inst.save()
                pizzaprice = round(pizzaprice*order_inst.quantity, 3)
                order_inst.pizza_price = pizzaprice
                order_inst.save()
                return redirect('orders')
    return redirect('orders')

def decreament(request):
    if request.method == 'POST':
        if 'order_id' in request.POST:
            order_id = request.POST['order_id']
            order = Order.objects.filter(id=order_id)
            pizzaname = request.POST['pizza_name']
            order_inst = order.first()
            pizzaprice = order_inst.pizza_price

            if order_inst.quantity == 1:
                order_inst.quantity = 0
                order_inst.save()
                order_inst.delete()
                return redirect('orders')
            else:
                order_quantity = order_inst.quantity
                order_quantity -= 1
                order_inst.quantity = order_quantity
                order_inst.save()

                pizza_price = Pizza.objects.filter(pizza_name = pizzaname).first().pizza_price
                pizzaPrice = round(order_quantity*pizza_price,3)
                order_inst.pizza_price = pizzaPrice
                order_inst.save()
                return redirect('orders')
    return redirect('orders')

def deleteOrder(request):
    if request.method == 'POST':
        if 'order_id' in request.POST:
            order_id = request.POST['order_id']
            current_user = request.user
            current_order = Order.objects.get(id=order_id)
            current_order.delete()
            return redirect('orders')

def deleteallOrders(request):
    if request.method == 'POST':

        current_user = request.user
        current_order = Order.objects.filter(user = current_user)
        current_order.delete()
        return redirect('orders')

def orderConfirmed(request):
    if request.method == 'POST':
        current_user = request.user
        allorders = Order.objects.filter(user=current_user).update(order_confirmed = True)
        return redirect('orders')
        

def menu(request):
    try:
        
        if request.user:
            pizzas = Pizza.objects.all()
            current_user = request.user.username
            user = User.objects.filter(username = current_user).first()
            order = Order.objects.filter(user = user)
            #total no of orders
            if request.user and request.user != AnonymousUser:
                
                current_user = request.user
                ordersOfCurrentuser = Order.objects.filter(user = current_user)
                totalOrderList = []

                for pizzaOrder in ordersOfCurrentuser:
                    quantity = pizzaOrder.quantity
                    totalOrderList.append(quantity)

                totalOrders = sum(totalOrderList)
            else:
                totalOrders = 0
        
            ordersOfCurrentuser = Order.objects.filter(user = current_user)
            
            firstobjectofCurrentuser = ordersOfCurrentuser.first() 
        
    
            try:
                
                if request.method == 'POST':
                    if 'sno' in request.POST:
                        sno = request.POST['sno']
                    
                        #user_logedin = request.POST['user_logedin']
                        pizza = Pizza.objects.filter(sno = sno).first()
                
                        p_name = pizza.pizza_name
                        p_desc = pizza.pizza_desc
                        p_price = pizza.pizza_price
                        allorders = Order.objects.filter(user = user, pizza_name = p_name)
                        if not allorders:

                            order = Order(pizza_name = p_name, pizza_desc = p_desc, pizza_price = p_price, user = user)
                            order.save()
                            return redirect('menu')
                        else:
                            order_ = Order.objects.filter(user=user,pizza_name=p_name).first()
                            order_quantity = order_.quantity
                            
                            if order_quantity == 0:
                                order_.quantity = 1
                                order_.save()
                                return redirect('menu')
                            else:
                                order_quantity += 1
                                print(order_quantity)
                                order_.quantity = order_quantity
                                order_.save()
                                return redirect('menu')

                else:
                    print("request is not POST")

                
                
            except Exception:
                
                return redirect('menu')


    except Exception:
        messages.warning(request,'Please login to continue !')
        return redirect('login_data')
    pizzas = Pizza.objects.all()
    context = {
                'pizzas':pizzas, 
                'totalOrders':totalOrders,
                'firstobjectofCurrentuser': firstobjectofCurrentuser,
               }
    return render(request,'home/menu.html',context)

def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            f_name = request.POST['f_name']
            l_name = request.POST['l_name']
            email = request.POST['email']
            username = request.POST['username']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']
            if pass1 == pass2:
                try:
                    user = User.objects.create_user(username,email,pass1)
                    user.first_name = f_name
                    user.last_name = l_name
                    user.save()
                except:
                    messages.warning(request,'registration failed')
                user_login = authenticate(username = username, password = pass1)
                if user_login is not None:
                    login(request,user_login)
            else:
                
                messages.warning(request,"passwords don't match")
                return redirect('/signup/')
    else:
        return redirect("home")

    return render(request,'home/signup.html')

def login_data(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            user_name = request.POST['user_name']
            user_pass = request.POST['user_pass']

            user = authenticate(username = user_name, password = user_pass)
            if user is not None:
                login(request, user)
                messages.success(request,'login successful')
                return redirect("/home/")
            else:
                messages.warning(request, 'Invalid login credentials')
                return redirect("/login_data/")
    else:
        return redirect("home")

    return render(request,'home/login.html')

def profile(request):

    try:
        if request.user.is_authenticated:
            current_user = request.user
            form = ProfileForm(instance=current_user)

            if request.method == 'POST':
                try:
                    profile_image = request.FILES['profile_image']
                    profile = Profile(user=current_user,profile_image=profile_image)
                    profile.save()
                    messages.success(request, 'Profile pic uploaded successfully !')
                except Exception:
                    return redirect('profile')
            profile_obj = Profile.objects.filter(user=current_user)
            if profile_obj:
                profile_image_display = profile_obj.last()
                profile_image_url = profile_image_display.profile_image
            else:
                profile_image_url = "images/defaultuser.png"
            address = Address.objects.filter(user=current_user).first()
            if address:
                address_display = address.address
            else:
                address_display = "please provide your current address"
            context = {
            'profile_image_url':profile_image_url,
            'form':form,
            'address_display':address_display
            }
            return render(request,'home/profile.html',context)
    except Exception:
        return redirect('profile')


def address(request):
    current_user = request.user
    if request.method == 'POST':
        if 'address_area' in request.POST:
            address_area = request.POST['address_area']

            if not Address.objects.filter(user=current_user).first():
                address = Address(user = current_user, address = address_area)
                address.save()
                messages.success(request,'Address uploaded successfully')
                return redirect('profile')
            else:
                address = Address.objects.filter(user = current_user).update(address=address_area)
                messages.success(request, 'address updated successfully')
                return redirect('profile')
            
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        messages.warning(request,'you are loged out')
        return render(request,'home/login.html')
    
def contact(request):
    if request.method == 'POST':
        if 'query_details' in request.POST:
            query_details = request.POST['query_details']
            contact = Contact(user = request.user, query = query_details)
            contact.save()
            messages.success(request,'Your query has been sent successfully !')
    return render(request,'home/contact.html')