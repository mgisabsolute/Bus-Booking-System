from django.urls import path
from . import views
from myapp.views import cancel_bus_admin

urlpatterns = [
    path('', views.home, name="home"),
    path('findbus', views.findbus, name="findbus"),
    path('bookings', views.bookings, name="bookings"),
    path('cancellings', views.cancellings, name="cancellings"),
    path('seebookings', views.seebookings, name="seebookings"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('success', views.success, name="success"),
    path('signout', views.signout, name="signout"),
    path('wallet/', views.wallet_view, name='wallet_view'),
    path('wallet/add/', views.add_funds, name='add_funds'),
    path('admin/cancel-bus/', cancel_bus_admin, name='cancel_bus_admin'),

]