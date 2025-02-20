from django.contrib import admin
from .models import Bus, User, Book, Wallet

class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_name', 'source', 'dest', 'get_seat_class_display', 'nos', 'rem', 'price', 'date', 'time')
    list_filter = ('seat_class', 'source', 'dest', 'date')
    search_fields = ('bus_name', 'source', 'dest')

class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'bus_name', 'get_seat_class_display', 'source', 'dest', 'nos', 'price', 'date', 'status')
    list_filter = ('seat_class', 'status', 'date')
    search_fields = ('name', 'email', 'bus_name')

# Register your models here.
admin.site.register(Bus, BusAdmin)
admin.site.register(User)
admin.site.register(Book, BookAdmin)
admin.site.register(Wallet)

