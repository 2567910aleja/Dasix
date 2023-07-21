from django.views.generic import *

class IndexView(TemplateView):
    template_name='index.html'