from django.contrib import admin

from checkout_app.models import ProductOrder, OrdersFileList

admin.site.register(ProductOrder)
admin.site.register(OrdersFileList)
