from django.contrib import admin

# Register your models here.
from .models import Users,Category,Posts
admin.site.register(Users)
admin.site.register(Category)
admin.site.register(Posts)