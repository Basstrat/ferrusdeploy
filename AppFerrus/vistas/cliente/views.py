from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required, permission_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from AppFerrus.models import Cliente
from AppFerrus.forms import ClienteForm
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect





    #vista basada en clases
class Clientelistview(ListView):
    model = Cliente
    template_name = 'cliente/lista.html' # este es el que uso para mi listado

    #metodos dispatch, este redireciona para post or get
     #metodo para confirmar si esta logeado
    #@method_decorator(csrf_exempt) 
    @method_decorator(permission_required('AppFerrus.view_cliente'))
    def dispatch(self, request, *args, **kwargs): 
        return super().dispatch(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs): # prueba metodo post
        data = {}
        try:
            data = Cliente.objects.get(pk=request.POST['id']).toJSON()  #aqui pido mi informacion a mis modelos
       #aqui lo que quiero que me devuelva
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Listado clientes'
        context['crear_url'] =  reverse_lazy('clienteañadirregistro')
        return context 


#este es para mi formulario
class ClienteCreateView(CreateView):
    model = Cliente #aqui llamo a mi modelo
    form_class = ClienteForm #aqui llamo a mi form de fomrs.py
    template_name = 'cliente/crearregistro.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('clientelista') #direccion hacia donde voy a redireccionar
    
    #aqui viy a definir para cuando se aguarde un dato repetido
  

    @method_decorator(permission_required('AppFerrus.add_cliente'))
    def dispatch(self, request, *args, **kwargs): 
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(request, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Crear un cliente' #titulo de la tabla y pestaña
        return context 
        #los decoradores pueden modificar de una forma dinamica una funcion



#para editar o actualizar registros
class ClienteUpdateView(UpdateView):
    model = Cliente #aqui llamo a mi modelo
    form_class = ClienteForm #aqui llamo a mi form de fomrs.py
    template_name = 'cliente/crearregistro.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('clientelista') #direccion hacia donde voy a redireccionar
    @method_decorator(permission_required('AppFerrus.change_cliente'))
    def dispatch(self, request, *args, **kwargs): 
        return super().dispatch(request, *args, **kwargs)
        
    def get_context_data(  self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Edicion'
        context['crear_url'] =  reverse_lazy('clienteañadirregistro')
        return context 

#vista para eliminar registros
class ClienteDeleteView(DeleteView):
    model = Cliente #aqui llamo a mi modelo
    template_name = 'cliente/eliminaregistro.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('clientelista') #direccion hacia donde voy a redireccionar
    
    @method_decorator(permission_required('AppFerrus.delete_cliente'))
    def dispatch(self, request, *args, **kwargs): 
        return super().dispatch(request, *args, **kwargs)

    def get_context_data( self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion'
        context['crear_url'] =  reverse_lazy('clienteeliminaregistro')
        context['lista_url'] = self.success_url
        return context 