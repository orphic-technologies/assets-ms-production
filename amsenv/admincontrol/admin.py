from django.contrib import admin
from .models import User
from products.models import Vendor, Product, AssestAssign, Specifications, AssestReturn, Image, Location

admin.site.register(User)
admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(AssestAssign)
admin.site.register(Specifications)
admin.site.register(AssestReturn)
admin.site.register(Image)
admin.site.register(Location)
