from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from AppFerrus.models import Proveedores
from AppFerrus.forms import ProveedoresForm
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import permission_required




    #vista basada en clases
class Proveedoreslistview(ListView):
    model = Proveedores
    template_name = 'proveedor/lista.html' # este es el que uso para mi listado

    #metodos dispatch, este redireciona para post or get
    #@method_decorator(login_required) metodo para confirmar si esta logeado
    @method_decorator(permission_required('AppFerrus.view_proveedores'))
    def dispatch(self, request, *args, **kwargs): 
        return super().dispatch(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs): # prueba metodo post
        data = {}
        try:
            data = Proveedores.objects.get(pk=request.POST['id']).toJSON()  #aqui pido mi informacion a mis modelos
       #aqui lo que quiero que me devuelva
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Listado proveedores'
        context['crear_url'] =  reverse_lazy('proveedoresañadirregistro')
        return context 


#este es para mi formulario
class ProveedoresCreateView(CreateView):
    model = Proveedores #aqui llamo a mi modelo
    form_class = ProveedoresForm #aqui llamo a mi form de fomrs.py
    template_name = 'proveedor/crearregistro.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('proveedoreslista') #direccion hacia donde voy a redireccionar
    
    #aqui viy a definir para cuando se aguarde un dato repetido
  
    @method_decorator(permission_required('AppFerrus.add_proveedores'))
    def dispatch(self, request, *args, **kwargs): 
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Crear un proveedor' #titulo de la tabla y pestaña
        return context 
        #los decoradores pueden modificar de una forma dinamica una funcion



#para editar o actualizar registros
class ProveedoresUpdateView(UpdateView):
    model = Proveedores #aqui llamo a mi modelo
    form_class = ProveedoresForm #aqui llamo a mi form de fomrs.py
    template_name = 'proveedor/crearregistro.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('proveedoreslista') #direccion hacia donde voy a redireccionar
    
    @method_decorator(permission_required('AppFerrus.change_proveedores'))
    def dispatch(self, request, *args, **kwargs): 
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Edicion'
        context['crear_url'] =  reverse_lazy('proveedoresañadirregistro')
        return context 

#vista para eliminar registros
class ProveedoresDeleteView(DeleteView):
    model = Proveedores #aqui llamo a mi modelo
    template_name = 'proveedor/eliminaregistro.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('proveedorlista') #direccion hacia donde voy a redireccionar
    
    @method_decorator(permission_required('AppFerrus.delete_proveedores'))
    def dispatch(self, request, *args, **kwargs): 
        return super().dispatch(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion'
        context['crear_url'] =  reverse_lazy('provedoreseliminaregistro')
        context['lista_url'] = self.success_url
        return context 