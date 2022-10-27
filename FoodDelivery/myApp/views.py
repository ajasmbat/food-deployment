from turtle import title
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


from .forms import AddListings, AddStore, UserForm 

from .models import Cart, Listings, Stores

# Create your views here.



def greeting(request):

    return render(request,'greeting.html')


def index(request):
    
   
   
   
   
   
    return render(request,'index.html',context={})








@login_required
def home(request):


    
    if request.method == 'POST':

        store_form = AddStore(request.POST)

       

        if store_form.is_valid():

            new_form = Stores.objects.create(
                user = User.objects.get(pk = request.user.id),
                store_name = store_form.cleaned_data['store_name'],
                address = store_form.cleaned_data['address']
            )
            
            new_form.save()


        else:
            
            print(store_form.errors)
            print('not valid')

    else:

        store_form=AddStore()
        print('Blank Form')
    
    store_list = Stores.objects.filter(user=request.user)

    store_model = store_list
   
    store_dict = {
        'Stores': store_model,
        'Stores_form':store_form,
    }


    return render(request,'home.html',context=store_dict)

# store_id
def addListing(request,id):

    if request.method == 'POST':

        listing_form = AddListings(request.POST,request.FILES)

       

        if listing_form.is_valid():

            new_form = Listings.objects.create(
                store_id = id,
                item_name = listing_form.cleaned_data['item_name'],
                item_picture = listing_form.cleaned_data['item_picture'],
                item_description = listing_form.cleaned_data['item_description'],
                quantity = listing_form.cleaned_data['quantity']
                
            )

            new_form.save()

            list = Listings.objects.filter(store_id=id)
            listing = list

            



             
            
            


        else:
            
            print(listing_form.errors)
            print('not valid')

    else:

        listing_form=AddListings()
        print('Blank Form')

        list = Listings.objects.filter(store_id=id)
        listing = list
    
    

    
   
    store_dict = {
        
        'listing_form':listing_form,
        'listing':listing
    }


    return render(request,'createlisting.html',context=store_dict)





def delete(request, id):
    data = get_object_or_404(Stores, id=id) 
    data.delete()
    print('delete')
    return redirect('home')


def deleteListing(request,id):
    data = get_object_or_404(Listings,id=id)
    data.delete()
    print('delete')
    return redirect(request.META['HTTP_REFERER'])



def stores(request):


    store_list = Stores.objects.order_by('store_name')

    store_model = store_list
   
    store_dict = {
        'Stores': store_model}


    return render(request,'stores.html',context=store_dict)

    


def storesList(request,id):

    data = Listings.objects.filter(store_id=id)
    print(data)
   
    
    
    return render(request,'listings.html',context={"listings":data})

# (login_url='user_login')

@login_required
def cart(request):

    cart_model = Cart.objects.filter(user=request.user)


    return render(request,'cart.html',context={'cart_item':cart_model})
    
    

@login_required
def AddCart(request, id):


    current_user = request.user

   
    

    store_form = Cart(user_id=current_user.id,item_id=id)

    

    store_form.save()






    
   
    
    
    return redirect(request.META['HTTP_REFERER'])

def RemoveCart(request, id):


    

   
    

    data = Cart.objects.get(id=id)
    print(data)

    data.delete()






    
   
    
    
    return redirect(request.META['HTTP_REFERER'])



def register(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        

        # Check to see both forms are valid
        if user_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()


            login(request,user)

            

            registered = True

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'registration.html',
                          {'user_form':user_form, 'registered':registered})


def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('stores'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'login.html', {})



@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('stores'))