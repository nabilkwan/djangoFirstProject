from django import forms
from .models import Inbound, Item, Outbound

class InboundForm(forms.ModelForm):
    product_sku = forms.ModelChoiceField(
        queryset=Item.objects.all(),
        label = "Product SKU",
        empty_label = "Select Product SKU"
    )
    reference = forms.CharField(label="Reference", max_length=200)
    quantity = forms.IntegerField(label="Quantity")
    location = forms.CharField(label="Location", max_length=200)
    remarks = forms.CharField(required=False,label="Remarks", max_length=200)
    class Meta:
        model = Inbound
        fields = ['product_sku', 'reference', 'quantity', 'location', 'remarks']
        
class OutboundForm(forms.ModelForm):
    product_sku = forms.ModelChoiceField(
    queryset=Item.objects.all(),
    label = "Product SKU",
    empty_label = "Select Product SKU"
    )
    reference = forms.CharField(label="Reference", max_length=200)
    quantity = forms.IntegerField(label="Quantity")
    destination = forms.CharField(label="Destination", max_length=200)
    remarks = forms.CharField(required=False,label="Remarks", max_length=200)
    class Meta:
        model = Outbound
        fields = ['product_sku', 'reference', 'quantity', 'destination', 'remarks']
        
class InboundEditForm(forms.ModelForm):
    class Meta:
        model = Inbound
        fields = ['product_sku', 'reference', 'quantity', 'location', 'remarks']
        
class OutboundEditForm(forms.ModelForm):
    class Meta:
        model = Outbound
        fields = ['product_sku', 'reference', 'quantity', 'destination', 'remarks']        