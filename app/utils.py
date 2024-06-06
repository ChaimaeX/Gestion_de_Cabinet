import datetime
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)
from datetime import datetime
from .models import *
from num2words import num2words
def pagination(request, factures):
    # default_page 
        default_page = 1 

        page = request.GET.get('page', default_page)

        # paginate items

        items_per_page = 5

        paginator = Paginator(factures, items_per_page)

        try:

            items_page = paginator.page(page)

        except PageNotAnInteger:

            items_page = paginator.page(default_page)

        except EmptyPage:

            items_page = paginator.page(paginator.num_pages) 

        return items_page    



def get_facture(pk):
    """ get invoice fonction """

    obj = Facture.objects.get(pk=pk)
    articles = FactureProduct.objects.filter(facture=pk)
    nombre = str(obj.TTC)
    parties = nombre.split('.')
    lettres_entier = num2words(parties[0], lang='fr')
    lettres_decimal = num2words(parties[1], lang='fr')


    context = {
        'obj': obj,
        'articles': articles,
        'lettres_entier':lettres_entier,
        'lettres_decimal':lettres_decimal,
    }

    return context


        
import datetime

class MaClasse:
    # Variables statiques pour le numéro de facture et l'année actuelle
    numero_facture = 0
    annee_actuelle = datetime.datetime.now().year

    def __init__(self):
        # Vérifier si l'année actuelle a changé
        if datetime.datetime.now().year > MaClasse.annee_actuelle:
            MaClasse.numero_facture = 0  # Réinitialiser le numéro de facture à zéro
            MaClasse.annee_actuelle = datetime.datetime.now().year  # Mettre à jour l'année actuelle

        # Incrémenter le numéro de facture
        MaClasse.numero_facture += 1

        # Assigner le numéro de facture à cet objet
        self.numero_facture = MaClasse.numero_facture

   

