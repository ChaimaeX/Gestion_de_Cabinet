from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Facture(models.Model):
     ModeType={
          ('C', _('CHEQUE')),
          ('E', _('ESPACE')),
     }
    
     client = models.CharField(max_length=132)
     Nemero = models.IntegerField()
     facture_date_time = models.DateTimeField(auto_now_add=True)
     # save_by = models.ForeignKey(User, on_delete=models.PROTECT )
     total =  models.DecimalField(max_digits =10 , decimal_places=2)# Exemple avec 10 chiffres au maximum et 2 chiffres après la virgule
     last_update_date = models.DateTimeField(null = True, blank=True)
     paid = models.BooleanField(default=False)
     TTC = models.DecimalField(max_digits =10 , decimal_places=2)
     TYPE =  models.CharField(max_length=1, choices=ModeType)

     class Meta:
          verbose_name = "Facture"
          verbose_name_plural ="Factures"

     def __str__(self):
         return f"{self.client}"
     @property
     def get_totals(self):
          produits = self.FactureProduct_set.all()
          ttc = self.total + sum(produit.tva for produit in produits)
    
          return ttc
     def get_ModeReglement_display(self):
        return dict(self.ModeType).get(self.ModeReglement, '')
     
class Chef(models.Model):
    name = models.CharField(max_length=132)
    password = models.CharField(max_length=255)
    class Meta:
        verbose_name = "chef"

    def __str__(self):
          return self.name

class Produit(models.Model):
     """
     une facture associet a plusieur produit
     une produit associet a un facture
     # """
     
     # facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
     category =models.TextField(max_length=100)
     name = models.TextField(max_length=32)
     quantity = models.IntegerField()
     price =  models.DecimalField(max_digits =10 , decimal_places=2)
     total = models.DecimalField(max_digits =10 , decimal_places=2)
     Important = models.BooleanField(default=False)

     class Meta:
          verbose_name ="Produit"
          verbose_name_plural ="Produits"
     
     def __str__(self):
          return self.name

     @property
     def get_total(self):
        total = self.quantity *self.price

class FactureProduct(models.Model):
    
    
     facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
     produit = models.ForeignKey(Produit,on_delete=models.CASCADE)
     quantity_achat = models.IntegerField()
     price_finich = models.DecimalField(max_digits =10, decimal_places=2)
     total_a = models.DecimalField(max_digits =10, decimal_places=2)
     TTVA = models.IntegerField()
     TVA =  models.DecimalField(max_digits =10, decimal_places=2, )
     # TTC = models.DecimalField(max_digits =10 , decimal_places=2)
    


# class ProductImportant(models.Model):
#      # name = models.TextField(max_length=32)
#      id_product = models.ForeignKey(Produit,on_delete=models.CASCADE)
#      min_quantite = models.IntegerField()
     
#      def __str__(self):
#           return self.id_product.name