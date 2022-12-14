from django.contrib import admin

# Register your models here.
from products.models import *
admin.site.register(book)
admin.site.register(Catecory)
admin.site.register(Comment)
admin.site.register(ForbiddenWords)
admin.site.register(Profile)

