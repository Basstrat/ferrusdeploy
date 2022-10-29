from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from AppFerrus.models import Persona
from AppFerrus.forms import PersonaForm
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import permission_required



    #vista basada en clases
class Personalistview(ListView):
    model = Persona
    template_name = 'persona/lista.html' # este es el que uso para mi listado

    #metodos dispatch, este redireciona para post or get
    #@method_decorator(login_required) metodo para confirmar si esta logeado
    @method_decorator(permission_required('AppFerrus.view_persona')) 
    def dispatch(self, request, *args, **kwargs): 
        return super().dispatch(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs): # prueba metodo post
        data = {}
        try:
            data =Persona.objects.get(pk=request.POST['id']).toJSON()  #aqui pido mi informacion a mis modelos
       #aqui lo que quiero que me devuelva
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Listado personas'
        context['crear_url'] =  reverse_lazy('personaañadirregistro')
        return context 


#este es para mi formulario
class PersonaCreateView(CreateView):
    model = Persona #aqui llamo a mi modelo
    form_class = PersonaForm #aqui llamo a mi form de fomrs.py
    template_name = 'persona/crearregistro.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('personalista') #direccion hacia donde voy a redireccionar
    
    #aqui viy a definir para cuando se aguarde un dato repetido
    @method_decorator(permission_required('AppFerrus.add_persona'))
    def dispatch(self, request, *args, **kwargs): 
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Crear una persona' #titulo de la tabla y pestaña
        return context 
        #los decoradores pueden modificar de una forma dinamica una funcion



#para editar o actualizar registros
class PersonaUpdateView(UpdateView):
    model = Persona #aqui llamo a mi modelo
    form_class = PersonaForm #aqui llamo a mi form de fomrs.py
    template_name = 'persona/crearregistro.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('personalista') #direccion hacia donde voy a redireccionar
    
    @method_decorator(permission_required('AppFerrus.change_persona'))
    def dispatch(self, request, *args, **kwargs): 
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Edicion'
        context['crear_url'] =  reverse_lazy('personaañadirregistro')
        return context 

#vista para eliminar registros
class PersonaDeleteView(DeleteView):
    model = Persona #aqui llamo a mi modelo
    template_name = 'persona/eliminaregistro.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('personalista') #direccion hacia donde voy a redireccionar
    
    @method_decorator(permission_required('AppFerrus.delete_persona'))
    def dispatch(self, request, *args, **kwargs): 
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion'
        context['crear_url'] =  reverse_lazy('eliminaregistro')
        context['lista_url'] = self.success_url
        return context 