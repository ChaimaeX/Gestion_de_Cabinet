import datetime
import os
from django.shortcuts import render
from django.views import View
from .models import*
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.core.paginator import  (Paginator,EmptyPage)
from .utils import pagination, get_facture,MaClasse
from django.template.loader import get_template
import pdfkit
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

class HomeView(View):
    template_name="home.html"
    factures = Facture.objects.all().order_by('-facture_date_time')
    
    context={
        'factures': factures    
    }
    def get(self, request, *args, **kwargs):
       
        items = pagination(request, self.factures)
        self.context['factures'] = items
        
        return render(request, self.template_name,self.context)
    def post(self, request, *args, **kwargs):
        #modifier un facture
         factures = Facture.objects.all().order_by('-facture_date_time')
         self.context['factures'] = factures
         if request.POST.get('id_modified'):

            paid = request.POST.get('modified')

            try: 

                obj = Facture.objects.get(id=request.POST.get('id_modified'))

                if paid == 'True':

                    obj.paid = True

                else:

                    obj.paid = False 

                obj.save() 

                messages.success(request, ("Changement effectué avec succès.")) 
            except Exception as e:   
                  messages.error(request, f"Désolé, une erreur s'est produite. {e}.")  
         
        
         # deleting an invoice    

         if request.POST.get('id_supprimer'):

            try:

                obj = Facture.objects.get(pk=request.POST.get('id_supprimer'))

                obj.delete()

                messages.success(request, ("La suppression a été effectuée avec succès."))   
           
            except Exception as e:
                 messages.error(request, f"Désolé, une erreur s'est produite. {e}.") 

            items = pagination(request, self.factures)
            self.context['factures'] = items
                    

         return render(request, self.template_name,self.context)
""" ajouter facture"""
class addFactureView(View):
    template_name="addFacture.html"
    product = Produit.objects.all()
    context ={
        'produits': product
    }
    
    def get(self, request, *args, **kwargs):
        product = Produit.objects.all().order_by('name')
        self.context['produits'] = product
        return render(request, self.template_name,self.context)
    
    @transaction.atomic()
    def post(self,request,*args,**kwags):
       items=[]  
       Qte = Produit.quantity
       MTV = 0
      

       try:
         client = request.POST.get('client')
         produits = request.POST.getlist('produit')
         qty = request.POST.getlist('qty')
         price = request.POST.getlist('unit')
         total_c = request.POST.getlist('total-a')
         type = request.POST.get('type')
         paid = request.POST.get('paid')
         total = request.POST.get('total')
         TTVA = request.POST.getlist('TTVA')
         print()
         cpt = 0
         for produit_id, qte in zip(produits, qty):
           produit = Produit.objects.get(id=produit_id)
           if int(qte) <= produit.quantity:
               cpt=cpt+1
                  
               if cpt == len(produits):
                 if not paid:
                   paid ='False'
                 facture1 = MaClasse()
                 print(facture1.numero_facture)
                 facture_object={
                    'Nemero': facture1.numero_facture,
                    'client':client,
                    'total': float(total),
                    'paid': paid,
                    'TTC':0,
                    'TYPE': type,
                    
                 }
                 facture = Facture.objects.create(**facture_object)
                 
                 print(total_c)
                 for produit_id, qte, prix, total_b,taux in zip(produits, qty , price,total_c,TTVA):
          
                   produit = Produit.objects.get(id=produit_id)

                   TVA = float(total_b) * (int(taux) / 100)
                   MTV += TVA
                
                   TTC = float(total) + MTV
                   
                    
                   data = FactureProduct(
                      facture_id = facture.id,
                      produit =  produit,
                      quantity_achat = qte,
                      price_finich = float(prix),
                      total_a = float(total_b),
                      TTVA = taux,
                      TVA = TVA,
                     
                    #   TTC = TTC,
                    )
                   items.append(data)
                   produit.quantity -= int(qte)
                   produit.total -= int(qte)*produit.price
                   produit.save()

                 obj = Facture.objects.get(id=facture.id)
                 obj.TTC=TTC
                 obj.save()
       
         
                    
                 
        
         
                 created = FactureProduct.objects.bulk_create(items) 
                 if created:
                  messages.success(request,'Les données ont été enregistrées avec succès..')
                 
       
           else:
              messages.error(request, f"Quantité insuffisante pour {produit.name}")
          
       except Exception as e :
            messages.error(request , f"Error ..{e}")
            #code incomplet Qte n9soha mn bd
       return render(request ,self.template_name,self.context)
     






""" View stock""" 
class ConsulterStockView(View):
     template_name="stock.html"
     Produits = Produit.objects.all()
     context ={
         'product' : Produits
     }
     def get(self, request, *args, **kwargs):
        products = Produit.objects.all() 
        important_products = Produit.objects.filter(Important=True)
        
        # Récupération des produits dont la quantité est presque épuisée
        items = []
        for product in important_products:
            if 0 < product.quantity < 4:
                items.append(product.name)
        
        # Affichage du message d'avertissement
        if items:
            messages.warning(request, f"La quantité de {', '.join(items)} est presque épuisée.")
        
        self.context['product'] = products
        return render(request, self.template_name, self.context)
     
     def post(self, request, *args, **kwargs):
          if request.POST.get('id_sup'):
            try:
          
               obj = Produit.objects.get(pk= request.POST.get('id_sup'))
               print(obj)
               obj.delete()
               messages.success(request, ("La suppression a été effectuée avec succès."))   
               product = Produit.objects.all()
               self.context['product'] = product
     
            except Exception as e:
                messages.error(request, f"Désolé, l'erreur est : {e}.")  
        
            return render(request, self.template_name,self.context)
     
""" update produit"""
class UpProduitView(View):
    template_name = "upProduct.html"
    product = Produit.objects.all()
    context ={
        'product':product
    }
    def get(self,request,*args,**kwargs):
        
         return render(request,self.template_name,self.context)  
      
    def post(self,request,*args,**kwargs):
        # print(request.POST.get('update'))
        # id = request.POST.get('update')
        if request.POST.get('update'):
            obj = Produit.objects.get(pk= request.POST.get('update'))
            self.context['product'] = obj
        else:
         try:
            title = request.POST.get('title')
            price = request.POST.get('price')
            qantite = request.POST.get('qantite')
            total = request.POST.get('total')
            category = request.POST.get('category')
            Important = request.POST.get('important')
            obj_secondaire =self.context['product']
            print(obj_secondaire.id)
            print(Important)
            obj = Produit.objects.get(pk=obj_secondaire.id)
            if not Important:
                Important=False
            obj.category = category
            obj.name = title
            obj.quantity = qantite
            obj.price = float(price)
            obj.total = float(total)
            obj.Important = Important
    
            # Sauvegarder les modifications
            obj.save()
            self.context['product'] = obj
            messages.success(request, 'Produit mis à jour avec succès.')
            return redirect('Stock')
           
         except Exception as e :
             messages.error(request, 'Une erreur s\'est produite lors de la mise à jour du produit : {}'.format(str(e)))
         
        return render(request,self.template_name,self.context)
    
""" vue facture"""
class InvoiceVisualizationView(View):

    template_name = 'facture.html'
    annee = datetime.datetime.now()
    annee_actuelle = annee.strftime("%y")
    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        
        context = get_facture(pk)
        context['annee'] = self.annee_actuelle
        return render(request, self.template_name,context)

def get_invoice_pdf(request, *args, **kwargs):
    """ generate pdf file from html file """

    pk = kwargs.get('pk')

    context = get_facture(pk)

    context['date'] = datetime.datetime.today()

    # get html file
    template = get_template('facture-pdf.html')

    # render html with context variables

    html = template.render(context)

    # options of pdf format 

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        "enable-local-file-access": ""
    }

    # generate pdf 

     # generate pdf 
    pdf = pdfkit.from_string(html, False, options)

    # Define the directory to save the PDF based on the invoice date
    invoice_date = Facture.objects.get(pk=pk).facture_date_time  # Assuming 'date' is the key for the invoice date in context
    year_folder = str(invoice_date.year)
    month_folder = str(invoice_date.month)
    directory = os.path.join('C:\\Users\\laptop\\Desktop\\Facture', year_folder, month_folder)

    # Create directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Define the file path
    file_path = os.path.join(directory, 'facture_{}.pdf'.format(pk))

    # Save the PDF file
    with open(file_path, 'wb') as f:
        f.write(pdf)

    # Create an HTTP response with the PDF file
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="facture_{}.pdf"'.format(pk)

    return response

class addProduitView(View):
    """ add un produit tout sumplement dans un navigateur """

    template_name = 'addProduct.html'
    def get(self,request,*args,**kwargs):
        return render(request, self.template_name)
    def post(self,request,*args,**kwargs):
        # if request.POST.get('update'):

        try: 
            name = request.POST.get('title')
            price = request.POST.get('price')
            quantity = request.POST.get('qantite')
            category = request.POST.get('category')
            Important = request.POST.get('Important')
            total = request.POST.get('total')
            print(name,price)
            if not Important:
                Important=False
            add_produit={
                'category':category,
                'name':name,
                'quantity':quantity,
                'price': float(price),
                'total':float(total),
                'Important':Important,
            }
            created = Produit.objects.create(**add_produit)
            if created:
                  messages.success(request,'data saved seccessfully..')
            else:
                  messages.error(request , 'Sorry Quantite insufisont ..')
           
        except Exception as e:
               messages.error(request,f"Error ....{e}")
        
        return render(request, self.template_name)
        
class LoginView(View):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
       try: 
          username = request.POST.get('username')
          password = request.POST.get('password')
          chef = Chef.objects.filter(name=username, password=password).first()
          if chef is not None:
            #   self.template_name = "html/index.html"
              return redirect('Home') 
          else:
              messages.warning(request, 'Username or password incorrect')
              return render(request, self.template_name)
       except Exception as e:
           messages.ERROR(request,'{e}')
      