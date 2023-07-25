from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView

# se puede hacer cualquiera de las dos formas(loginformview o loginformview2)

class LoginFormView(LoginView):
    template_name='login.html'

    def dispatch(self, request, *args, **kwargs):
        #if request.user.is_authenticated:
            #return redirect('erp:categoria_list')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='Iniciar sesion'
        return context
    
class LoginFormView2(FormView):
    template_name='login.html'
    form_class=AuthenticationForm
    success_url= reverse_lazy('erp:categoria_list')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.success_url)

    def dispatch(self, request, *args, **kwargs):
        #if request.user.is_authenticated:
            #return redirect('erp:categoria_list')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='Iniciar sesion'
        return context
    
class LogoutRedirectView(RedirectView):
  pattern_name = 'login'

  def dispatch(self, request, *args, **kwargs):
    logout(request)
    return super().dispatch(request, *args, **kwargs)