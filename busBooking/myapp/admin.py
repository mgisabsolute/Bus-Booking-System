from django.contrib import admin
from .models import Bus, User, Book
from .models import Wallet

# Register your models here.
admin.site.register(Bus)
admin.site.register(User)
admin.site.register(Book)
admin.site.register(Wallet)