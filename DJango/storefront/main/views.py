from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Item, Inbound, Category, Outbound
from .forms import InboundForm, OutboundForm, InboundEditForm, OutboundEditForm
from datetime import datetime

# Create your views here.


def home(request):
    return render(request, "main/home.html")

def inventory_operation(request, operation): #create inbound/outbound transaction
    if operation not in ['inbound', 'outbound']:
        return HttpResponseBadRequest("Invalid operation")

    Model = Inbound if operation == 'inbound' else Outbound
    Form = InboundForm if operation == 'inbound' else OutboundForm
    template = f"main/{operation}.html"

    items = Model.objects.all()

    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
            with transaction.atomic():
                item_operation = form.save()
                product = item_operation.product_sku
                if operation == 'inbound':
                    product.quantity += item_operation.quantity
                else:
                    product.quantity -= item_operation.quantity
                product.save()
            return redirect(operation)
    else:
        form = Form()

    context = {
        f'{operation}s': items,
        'form': form,
        'operation': operation
    }
    return render(request, template, context)

def inventory_table(request, operation, id):
    if operation not in ['inbound', 'outbound']:
        return HttpResponseBadRequest("Invalid operation")

    category = get_object_or_404(Category, id=id)
    items = Item.objects.filter(category=category)
    
    if operation == 'inbound':
        filtered_items = Inbound.objects.filter(product_sku__in=items)
        form = InboundEditForm()
        template = "main/inbound_table.html"
        context_key = "inbounds"
    else:  # outbound
        filtered_items = Outbound.objects.filter(product_sku__in=items)
        form = OutboundEditForm()
        template = "main/outbound_table.html"
        context_key = "outbounds"

    context = {
        context_key: filtered_items,
        "category": category,
        "operation": operation,
        "form": form
    }
    
    return render(request, template, context)

def update_record(request, operation):
    if operation not in ['inbound', 'outbound']:
        return HttpResponseBadRequest("Invalid operation")

    if request.method == "POST":
        id = request.POST.get('id')
        if operation == 'inbound':
            instance = get_object_or_404(Inbound, id=id)
            form = InboundEditForm(request.POST, instance=instance)
        else:
            instance = get_object_or_404(Outbound, id=id)
            form = OutboundEditForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "errors": form.errors})

    return HttpResponseBadRequest("Invalid request method")

def delete_record(request, operation):
    if operation not in ['inbound', 'outbound']:
        return HttpResponseBadRequest("Invalid operation")

    if request.method == "POST":
        id = request.POST.get('id')
        if operation == 'inbound':
            instance = get_object_or_404(Inbound, id=id)
        else:
            instance = get_object_or_404(Outbound, id=id)

        instance.delete()
        return JsonResponse({"success": True})

    return HttpResponseBadRequest("Invalid request method")



def item(request, id):
    category = get_object_or_404(Category, id=id)
    items = Item.objects.filter(category=category)
    return render(request, "main/item.html", {
        "category": category,
        "items": items
    })
    
def get_inventory_data(request):
    year = int(request.GET.get('year', datetime.now().year))
    
    inbound_data = (Inbound.objects
        .filter(date__year=year)
        .values('product_sku__category__category')
        .annotate(month=ExtractMonth('date'))
        .values('product_sku__category__category', 'month')
        .annotate(total=Sum('quantity'))
        .order_by('product_sku__category__category', 'month'))

    outbound_data = (Outbound.objects
        .filter(date__year=year)
        .values('product_sku__category__category')
        .annotate(month=ExtractMonth('date'))
        .values('product_sku__category__category', 'month')
        .annotate(total=Sum('quantity'))
        .order_by('product_sku__category__category', 'month'))

    categories = Category.objects.values_list('category', flat=True)
    
    inbound_result = []
    outbound_result = []

    for category in categories:
        inbound_category_data = [0] * 12
        outbound_category_data = [0] * 12

        for item in inbound_data:
            if item['product_sku__category__category'] == category:
                inbound_category_data[item['month'] - 1] = item['total']

        for item in outbound_data:
            if item['product_sku__category__category'] == category:
                outbound_category_data[item['month'] - 1] = item['total']

        inbound_result.append({
            'name': category,
            'data': inbound_category_data
        })
        outbound_result.append({
            'name': category,
            'data': outbound_category_data
        })

    return JsonResponse({
        'inbound': inbound_result,
        'outbound': outbound_result
    })


