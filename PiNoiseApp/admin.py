from django.contrib import admin

# Register your models here.
from .models import Users,Category,Posts,Reports
admin.site.register(Users)
admin.site.register(Category)



class ReportsAdmin(admin.ModelAdmin):
    list_display = ('title','author','reporter','reason')

admin.site.register(Reports, ReportsAdmin)

class PostsAdmin(admin.ModelAdmin):
    search_fields = ('^title','^author')
    list_display = ('Post_title','Post_author','Post_category')


admin.site.register(Posts,PostsAdmin)