from django.contrib import admin

from libraryApp.models import *

admin.site.register(Library)
admin.site.register(Librarian_Mangement)
admin.site.register(Books_Type)
admin.site.register(Library_Rules)
admin.site.register(Book_Detail)
admin.site.register(Issue_Book)
admin.site.register(Fine_History)



"""here register Inventory models"""

admin.site.register(Product_Type)
admin.site.register(Product_Detail)
admin.site.register(Break_product_Detail)
admin.site.register(Product_Request)



