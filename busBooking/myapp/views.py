from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Bus, Book
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal

from datetime import datetime
from django.contrib import messages
from django.shortcuts import render
from decimal import Decimal
from .models import Wallet


def home(request):
    if request.user.is_authenticated:
        return render(request, 'myapp/home.html')
    else:
        return render(request, 'myapp/signin.html')
    
@login_required(login_url='signin')
def findbus(request):
    context = {}
    if request.method == 'POST':
        source_r = request.POST.get('source')
        dest_r = request.POST.get('destination')
        date_r = request.POST.get('date')
        date_r = datetime.strptime(date_r,"%Y-%m-%d").date()
        year = date_r.strftime("%Y")
        month = date_r.strftime("%m")
        day = date_r.strftime("%d")
        bus_list = Bus.objects.filter(source=source_r, dest=dest_r, date__year=year, date__month=month, date__day=day)
        if bus_list:
            return render(request, 'myapp/list.html', locals())
        else:
            context['data'] = request.POST
            context["error"] = "No available Bus Schedule for entered Route and Date"
            return render(request, 'myapp/findbus.html', context)
    else:
        return render(request, 'myapp/findbus.html')


@login_required(login_url='signin')
def bookings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        seats_r = int(request.POST.get('no_seats'))
        bus = Bus.objects.get(id=id_r)

        if bus:
            total_cost = int(seats_r) * bus.price
            wallet, created = Wallet.objects.get_or_create(user=request.user)

            # Check if user has enough funds
            if wallet.balance < total_cost:
                messages.error(request, "Insufficient balance in wallet. Please add funds.")
                return redirect('wallet_view')

            if bus.rem >= seats_r:
                # Deduct the amount from wallet
                wallet.balance -= total_cost
                wallet.save()

                # Update seat availability
                rem_r = bus.rem - seats_r
                Bus.objects.filter(id=id_r).update(rem=rem_r)

                # Create booking record
                book = Book.objects.create(
                    name=request.user.username, email=request.user.email, userid=request.user.id,
                    bus_name=bus.bus_name, source=bus.source, busid=id_r,
                    dest=bus.dest, price=bus.price, nos=seats_r, date=bus.date, time=bus.time,
                    status='BOOKED'
                )

                messages.success(request, f"Booking successful! ₹{total_cost} has been deducted from your wallet.")
                return render(request, 'myapp/bookings.html', locals())

            else:
                messages.error(request, "Not enough seats available. Please select fewer seats.")
                return render(request, 'myapp/findbus.html', context)

    return render(request, 'myapp/findbus.html')



@login_required(login_url='signin')
def cancellings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')

        try:
            book = Book.objects.get(id=id_r)  # Find the booking
        except Book.DoesNotExist:
            messages.error(request, "Sorry, this booking does not exist.")
            return redirect('seebookings')

        try:
            bus = Bus.objects.get(id=book.busid)  # Find the corresponding bus
        except Bus.DoesNotExist:
            messages.error(request, "The bus for this booking no longer exists.")
            return redirect('seebookings')

        # Restore seat count
        rem_r = bus.rem + book.nos
        Bus.objects.filter(id=book.busid).update(rem=rem_r)

        # Refund the user
        refund_amount = book.price * book.nos
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        wallet.balance += refund_amount
        wallet.save()

        # Update booking status
        Book.objects.filter(id=id_r).update(status='CANCELLED', nos=0)

        messages.success(request, f"Your booking has been cancelled. ₹{refund_amount} has been refunded to your wallet.")
        return redirect('seebookings')

    return render(request, 'myapp/findbus.html')



@login_required(login_url='signin')
def seebookings(request,new={}):
    context = {}
    id_r = request.user.id
    book_list = Book.objects.filter(userid=id_r)
    if book_list:
        return render(request, 'myapp/booklist.html', locals())
    else:
        context["error"] = "Sorry no buses booked"
        return render(request, 'myapp/findbus.html', context)


def signup(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        email_r = request.POST.get('email')
        password_r = request.POST.get('password')
        user = User.objects.create_user(name_r, email_r, password_r, )
        if user:
            login(request, user)
            return render(request, 'myapp/thank.html')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signup.html', context)
    else:
        return render(request, 'myapp/signup.html', context)


def signin(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        password_r = request.POST.get('password')
        user = authenticate(request, username=name_r, password=password_r)
        if user:
            login(request, user)
            # username = request.session['username']
            context["user"] = name_r
            context["id"] = request.user.id
            return render(request, 'myapp/success.html', context)
            # return HttpResponseRedirect('success')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signin.html', context)
    else:
        context["error"] = "You are not logged in"
        return render(request, 'myapp/signin.html', context)


def signout(request):
    context = {}
    logout(request)
    context['error'] = "You have been logged out"
    return render(request, 'myapp/signin.html', context)


def success(request):
    context = {}
    context['user'] = request.user
    return render(request, 'myapp/success.html', context)




@login_required(login_url='signin')
def wallet_view(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    return render(request, 'myapp/wallet.html', {'wallet': wallet})

@login_required(login_url='signin')
def add_funds(request):
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount', 0))
        if amount > 0:
            wallet, created = Wallet.objects.get_or_create(user=request.user)
            wallet.add_funds(amount)
            messages.success(request, f'Successfully added ₹{amount} to your wallet')
        else:
            messages.error(request, 'Please enter a valid amount')
    return redirect('wallet_view')

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404

@login_required(login_url='signin')
@staff_member_required  # Ensures only admins can access this
def cancel_bus_admin(request):
    if request.method == "POST":
        bus_id = request.POST.get('bus_id')

        try:
            bus = Bus.objects.get(id=bus_id)
            bookings = Book.objects.filter(busid=bus_id, status="BOOKED")

            if not bookings:
                messages.info(request, "No active bookings found for this bus.")

            for booking in bookings:
                # Refund each passenger
                refund_amount = booking.price * booking.nos
                wallet, created = Wallet.objects.get_or_create(user=booking.userid)
                wallet.balance += refund_amount
                wallet.save()

                # Update booking status
                booking.status = "CANCELLED"
                booking.nos = 0
                booking.save()

            # Delete the bus
            bus.delete()

            messages.success(request, f"Bus '{bus.bus_name}' was canceled. All passengers have been refunded ₹{refund_amount} each.")
            return redirect('admin_dashboard')

        except Bus.DoesNotExist:
            messages.error(request, "Bus not found.")
            return redirect('admin_dashboard')

    return render(request, 'myapp/admin_cancel_bus.html')  # Create an admin UI for cancellation
