# -*- coding: UTF-8 -*-
from io import BytesIO
import csv

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import IntegerField, Sum, Case, When
from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic.edit import FormView

from openpyxl import load_workbook

from checkout_app.models import OrdersFileList, ProductOrder, \
    STATE_CREATED, STATE_STOPPED
from checkout_app.tasks import add_processing_of_product


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        else:
            return super(LoginFormView, self).dispatch(
                request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/login")


class FilesOfOrdersListView(LoginRequiredMixin, ListView):
    model = OrdersFileList
    template_name = 'file-list.html'
    context_object_name = 'results'
    paginate_by = settings.ROWS_ON_PAGE

    def get_queryset(self):
        qs = super(
            FilesOfOrdersListView,
            self).get_queryset().select_related().annotate(
                count_with_status_created=Sum(
                    Case(
                        When(product_orders__status=STATE_CREATED, then=1),
                        output_field=IntegerField())
                )
        ).order_by('-id')
        return qs


class OrdersListView(LoginRequiredMixin, ListView):
    model = ProductOrder
    template_name = 'orders-list.html'
    context_object_name = 'orders'
    paginate_by = settings.ROWS_ON_PAGE

    def get_queryset(self):
        return ProductOrder.objects.filter(
            orders_file_id=self.kwargs['pk']).order_by('id')


def upload_file_with_products(request):
    if request.method == "POST":
        if request.FILES['orders_list']:
            messages.success(request, 'Products from file was added')

            file_name = request.FILES['orders_list'].name
            orders_file_list = OrdersFileList(file_name=file_name)
            orders_file_list.save()

        file_in_memory = request.FILES['orders_list'].read()
        wb = load_workbook(filename=BytesIO(file_in_memory))
        ws = wb.active
        for i, row in enumerate(ws.rows):
            order = ProductOrder(
                id_in_file=i + 1,
                product_url=row[0].value,
                product_name=row[1].value,
                products_count=row[2].value,
                product_buyer=row[3].value,
                buyer_address=row[4].value,
                buyer_address2=row[5].value,
                buyer_city=row[6].value,
                buyer_state_code=row[7].value,
                buyer_postal_code=row[8].value,
                orders_file=orders_file_list)
            order.save()
            add_processing_of_product.delay(order.id)

    return HttpResponseRedirect('/')


def stop_not_processed_tasks(request, file_id=None):
    if file_id:
        product_order_list = ProductOrder.objects.filter(
            orders_file_id=file_id,
            status__in=[STATE_CREATED])
        for product_order in product_order_list:
            product_order.status = STATE_STOPPED
            product_order.save()
        messages.success(request, 'Not processed tasks are stopped')

    return HttpResponseRedirect('/')


def get_orders_in_xlsx(request, pk):
    try:
        fl = OrdersFileList.objects.get(pk=pk)
    except Exception:
        return HttpResponse('File do not exists')

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = \
        'attachment; filename="%s_employees.csv"' % fl.file_name

    qs = ProductOrder.objects.filter(orders_file_id=fl.id).order_by('id')

    writer = csv.writer(response, delimiter=';')
    for row in qs:
        product_url = row.product_url.encode(
            'utf-8').replace(';', '.') if row.product_url else None
        product_name = row.product_name.encode(
            'utf-8').replace(';', '.') if row.product_name else None
        products_count = row.products_count
        product_buyer = row.product_buyer.encode(
            'utf-8').replace(';', '.') if row.product_buyer else None
        buyer_address = row.buyer_address.encode(
            'utf-8').replace(';', '.') if row.buyer_address else None
        buyer_address2 = row.buyer_address2.encode(
            'utf-8').replace(';', '.') if row.buyer_address2 else None
        buyer_city = row.buyer_city.encode(
            'utf-8').replace(';', '.') if row.buyer_city else None
        buyer_state_code = row.buyer_state_code.encode(
            'utf-8').replace(';', '.') if row.buyer_state_code else None
        buyer_postal_code = row.buyer_postal_code.encode(
            'utf-8').replace(';', '.') if row.buyer_postal_code else None
        express_order_id = row.express_order_id.encode(
            'utf-8').replace(';', '.') if row.express_order_id else None
        delivery_time = row.delivery_time.encode(
            'utf-8').replace(';', '.') if row.delivery_time else None
        products_available = row.products_available
        status = row.get_status_display()
        writer.writerow([
            row.id_in_file, product_url, product_name, products_count,
            product_buyer, buyer_address, buyer_address2, buyer_city,
            buyer_state_code, buyer_postal_code, products_available,
            express_order_id, delivery_time, status])

    return response
