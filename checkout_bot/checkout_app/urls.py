from django.conf.urls import url
from checkout_app import views


urlpatterns = [
    url(r'^$', views.FilesOfOrdersListView.as_view(), name='file-list'),
    url(r'^login/$', views.LoginFormView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^orders-list/(?P<pk>[0-9]+)/$',
        views.OrdersListView.as_view(), name='orders-list'),
    url(r'^upload_file_with_products/$',
        views.upload_file_with_products, name='upload_file'),
    url(r'^get-orders/(?P<pk>[0-9]+)/$',
        views.get_orders_in_xlsx, name='get-orders'),
]
