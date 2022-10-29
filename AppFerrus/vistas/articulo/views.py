import json
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from AppFerrus.models import Articulo, Detarticulo, Material, Cliente
from AppFerrus.forms import ArticuloForm
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.db import transaction

class articulolistview(ListView):
    model = Articulo
    template_name = 'articulo/lista.html' # este es el que uso para mi listado

    @method_decorator(permission_required('AppFerrus.view_articulo'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = [] #es una array
                for i in Articulo.objects.all():
                    data.append(i.toJSON()) #incrustar datos dentro del array
            elif action == 'search_details_prod':
                data = []
                for i in Detarticulo.objects.filter(articulo_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False) #safe= false para que maneje varios datos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado articulos'
        context['entity'] = 'Articulos'
        context['create_url'] = reverse_lazy('articuloañadirregistro')
        context['list_url'] = reverse_lazy('articulolista')
        return context










#este es para mi formulario

class articuloCreateView(CreateView):
    model = Articulo #aqui llamo a mi modelo
    form_class = ArticuloForm #aqui llamo a mi form de fomrs.py
    template_name = 'articulo/crearregistro.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('articulolista') #direccion hacia donde voy a redireccionar
    
    #aqui viy a definir para cuando se aguarde un dato repetido
    @method_decorator(login_required)
    @method_decorator(permission_required('AppFerrus.add_articulo'))
    def dispatch(self, request, *args, **kwargs): 
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            print(request.POST)
            action = request.POST['action']
            if action == 'search_material': #la variable de mi form js
                data = [] #esto porque es un array
                materiales = Material.objects.filter(nombre__icontains=request.POST['variablebusqueda'])[0:10] #limitante de mostrar
                for i in materiales:
                    item = i.toJSON() #aqui llamo a mi json de mis modelos
                    item['value'] = i.nombre #esto me retornara lo que busco
                    data.append(item) #item es lo que va tirar la busqueda
            elif action == 'add':
                print(request.POST)
                cotizacion1 = json.loads(request.POST['cotizacion1'])
                articulo = Articulo()
                articulo.nombre = cotizacion1['nombre']
                articulo.fecha = cotizacion1['fecha']
                articulo.precio = float(cotizacion1['precio'])
                articulo.descripcion = cotizacion1['descripcion']
                articulo.mano_de_obra = float(cotizacion1['mano_de_obra'])
                articulo.otrosgastos = float(cotizacion1['otrosgastos'])
                articulo.porciento = float(cotizacion1['porciento'])
                articulo.save()
                
    #iterar materiales
                for i in cotizacion1['material']:
                    det = Detarticulo()
                    det.articulo_id = articulo.id
                    det.material_id = i['id']
                    det.cant = float(i['cant'])
                    det.precio = float(i['precio_unidad'])
                    det.subtotal = float(i['subtotal'])
                    det.save()
            else:
                data['error'] = 'Ha ocurrido un error 5'
        except Exception as e:
                data['error'] = str(e)
        return JsonResponse(data, safe=False) # para serializarlos cuando es coleccion de elemento ponemos false

    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Crear una Articulo'
        context['action'] = 'add'
        context['entity'] = 'Articulos' #titulo de la tabla y pestaña
        return context 
        #los decoradores pueden modificar de una forma dinamica una funcion


class articuloUpdateView(UpdateView):
    model = Articulo #aqui llamo a mi modelo
    form_class = ArticuloForm #aqui llamo a mi form de fomrs.py
    template_name = 'articulo/crearregistro.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('articulolista') #direccion hacia donde voy a redireccionar
    
    @method_decorator(permission_required('AppFerrus.change_articulo')) 
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            print(request.POST)
            if action == 'search_material': #la variable de mi form js
                data = [] #esto porque es un array
                materiales = Material.objects.filter(nombre__icontains=request.POST['variablebusqueda'])[0:10] #limitante de mostrar
                for i in materiales:
                    print(i.nombre)
                    item = i.toJSON() #aqui llamo a mi json de mis modelos
                    item['value'] = i.nombre #esto me retornara lo que busco
                    data.append(item) #item es lo que va tirar la busqueda
            elif action == 'searchdetails_prod':
                data= []
                for i in Detarticulo.objects.filter(articulo_id=request.POST['id']):
                    data.append(i.toJSON())

            elif action == 'edit': #para añadir mi registro
                print(request.POST)
                with transaction.atomic():
                    cotizacion1 = json.loads(request.POST['cotizacion1'])
                #cotizacion = Cotizacion.objects.gets(pk=self.get().id)
                    articulo = self.get_object()
                    articulo.nombre = cotizacion1['nombre']
                    articulo.fecha = cotizacion1['fecha']
                    articulo.precio = float(cotizacion1['precio'])
                    articulo.descripcion = cotizacion1['descripcion']
                    articulo.mano_de_obra = float(cotizacion1['mano_de_obra'])
                    articulo.otrosgastos = float(cotizacion1['otrosgastos'])
                    articulo.save()
                    articulo.detarticulo_set.all().delete() # para eliminar los detalles de la informacion anterior
                
    #iterar productos
                for i in cotizacion1['material']:
                    det = Detarticulo()
                    det.articulo_id = articulo.id
                    det.material_id = i['id']
                    det.cant = float(i['cant'])
                    det.precio = float(i['precio_unidad'])
                    det.subtotal = float(i['subtotal'])
                    det.save()
                
                    
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
                data['error'] = str(e)
        return JsonResponse(data, safe=False) # para serializarlos cuando es coleccion de elemento ponemos false

    def get_articulo_detalles(self): #para llamar mis productos
        data = [] #lo hago diccionario
        try:
            for i in Detarticulo.objects.filter(articulo_id=self.get_object().id):
                item = i.material.toJSON() #aqui pido mis articulos
                item['cant'] = i.cant #aqui pido mi cantidad
                data.append(item) #aqui llamo al diccionario
        except: 
            pass
        return data
        
    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Editar Articulo'
        context['entity'] = 'Articulo' #titulo de la tabla y pestaña
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_articulo_detalles(), default=str) # para convetir string
        return context 

class articulosUpdateView(UpdateView):
    model = Articulo #aqui llamo a mi modelo
    form_class = ArticuloForm #aqui llamo a mi form de fomrs.py
    template_name = 'articulo/editar.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('articulolista') #direccion hacia donde voy a redireccionar
    
    @method_decorator(permission_required('AppFerrus.change_venta'))
    def dispatch(self, request, *args, **kwargs): 
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Edicion'
        context['crear_url'] =  reverse_lazy('articuloañadirregistro')
        return context 


#vista para eliminar registros
class articuloDeleteView(DeleteView):
    model = Articulo #aqui llamo a mi modelo
    template_name = 'articulo/eliminaregistro.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('articulolista') #direccion hacia donde voy a redireccionar
    
    @method_decorator(permission_required('AppFerrus.delete_articulo')) 
    def dispatch(self, request, *args, **kwargs): 
        return super().dispatch(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion'
        context['crear_url'] =  reverse_lazy('articuloañadirregistro')
        context['lista_url'] = self.success_url
        return context 