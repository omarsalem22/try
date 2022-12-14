from products.models import Catecory

def menu_categories(request):
    categories = Catecory.objects.all()

    return {'menu_categories': categories}