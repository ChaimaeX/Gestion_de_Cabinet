from django.contrib import admin
from .models import *
# Register your models here.

class Adminchef(admin.ModelAdmin):
    list_display = ('name' ,'password')

class AdminFacture(admin.ModelAdmin):
    list_display= ('client','facture_date_time','total','paid','TYPE')
class AdminFactureProduct(admin.ModelAdmin):
     list_display=('facture','produit','quantity_achat','price_finich','total_a','TTVA','TVA','TTC')
class AdminProductImportant(admin.ModelAdmin):
    list_display= ('id_product','min_quantite')

admin.site.register(Chef,Adminchef)
admin.site.register(Facture,AdminFacture)
admin.site.register(Produit)
admin.site.register(FactureProduct)
# admin.site.register(ProductImportant,AdminProductImportant)