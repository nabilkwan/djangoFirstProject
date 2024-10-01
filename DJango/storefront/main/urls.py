from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'), #home page
    path("inbound/", views.inventory_operation, {'operation': 'inbound'}, name="inbound"), #inbound page
    path("outbound/", views.inventory_operation, {'operation': 'outbound'}, name="outbound"), #outbound page
    path("inbound/table/<int:id>", views.inventory_table, {'operation': 'inbound'}, name="inbound_table"), #combines electronic, furniture and clothing intbound
    path("outbound/table/<int:id>", views.inventory_table, {'operation': 'outbound'}, name="outbound_table"), #combines electronic, furniture and clothing outbound

    path("inbound/table/update/", views.update_record, {'operation': 'inbound'}, name="update_inbound"),
    path("outbound/table/update/", views.update_record, {'operation': 'outbound'}, name="update_outbound"),
    
    path("inbound/table/delete/", views.delete_record, {'operation': 'inbound'}, name="delete_inbound"),
    path("outbound/table/delete/", views.delete_record, {'operation': 'outbound'}, name="delete_outbound"),
    
    path("item/<int:id>", views.item, name="item"), # /item/
    path('get_inventory_data/', views.get_inventory_data, name='get_inventory_data'), #get data for graph
]