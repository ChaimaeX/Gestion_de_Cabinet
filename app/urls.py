from django.shortcuts import render
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('', views.LoginView.as_view(), name="Login"),
    path('home' ,views.HomeView.as_view() , name='Home'),
    path('ajouterFacture' ,views.addFactureView.as_view() , name='Facture'),
    path('Stock' ,views.ConsulterStockView.as_view() , name='Stock'),
    path('ajouterProduit' ,views.addProduitView.as_view() , name='Ajouter-produit'),
    path('update-product' ,views.UpProduitView.as_view() , name='upProduct'),
    path('facture/<int:pk>', views.InvoiceVisualizationView.as_view(), name="facture"),
    path('facture-pdf/<int:pk>', views.get_invoice_pdf, name="facture-pdf"),
    
]

urlpatterns+= static(settings.MEDIA_URL,documen_root=settings.MEDIA_ROOT)
urlpatterns+=staticfiles_urlpatterns()