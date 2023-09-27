from .models import Unit

def units(request):
    return {'units': Unit.objects.all()}
