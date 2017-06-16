from django.contrib import admin

from checkout_app.models import GoogleExpressUser, OrdersFileList, \
    ProductOrder


admin.site.register(ProductOrder)
admin.site.register(OrdersFileList)
admin.site.register(GoogleExpressUser)
