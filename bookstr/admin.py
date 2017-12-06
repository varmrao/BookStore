from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Customer)
admin.site.register(Owner)
admin.site.register(CreditCard)
admin.site.register(CrediCardOwner)
admin.site.register(BookBuyTrans)
admin.site.register(WrittenBy)
admin.site.register(BookReorder)
admin.site.register(BooksInReorder)
admin.site.register(Cart)
