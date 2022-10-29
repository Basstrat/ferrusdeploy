from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from AppFerrus.models import Ordendetrabajo, Cotizacion, Articulo
from AppFerrus.forms import ordendetrabajoForm
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.contrib.auth.decorators import permission_required
from AppFerrus.models import Articulo
from AppFerrus.models import Detordentrabajo
from django.db import transaction
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


class orden_trabajolistview(ListView):
    model = Ordendetrabajo
    template_name = 'orden_trabajo/lista.html' # este es el que uso para mi listado

    @method_decorator(permission_required('AppFerrus.view_ordendetrabajo'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = [] #es una array
                for i in Ordendetrabajo.objects.all():
                    data.append(i.toJSON()) #incrustar datos dentro del array
            elif action == 'search_details_prod':
                data = []
                for i in Detordentrabajo.objects.filter(ordendetrabajo_id=request.POST['id']):
                    data.append(i.toJSON())
                    print(i)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False) #safe= false para que maneje varios datos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado orden de trabajo'
        context['entity'] = 'Ordne de trabajo'
        context['create_url'] = reverse_lazy('ordentrabajocrear')
        context['list_url'] = reverse_lazy('ordentrabajolistado')
        return context







#este es para mi formulario

class orden_trabajoCreateView(CreateView):
    model = Ordendetrabajo #aqui llamo a mi modelo
    form_class = ordendetrabajoForm #aqui llamo a mi form de fomrs.py
    template_name = 'orden_trabajo/crearregistro.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('ordentrabajolistado') #direccion hacia donde voy a redireccionar
    @method_decorator(permission_required('AppFerrus.add_ordendetrabajo')) 
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    #aqui viy a definir para cuando se aguarde un dato repetido

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            print(request.POST)
            if action == 'search_articulo': #la variable de mi form js
                data = [] #esto porque es un array
                articulos = Articulo.objects.filter(nombre__icontains=request.POST['variablebusqueda'])[0:10] #limitante de mostrar
                for i in articulos:
                    print(i.nombre)
                    item = i.toJSON() #aqui llamo a mi json de mis modelos
                    item['value'] = i.nombre #esto me retornara lo que busco
                    item['cant'] = 1
                    data.append(item) #item es lo que va tirar la busqueda
            elif action == 'add': #para añadir mi registro
                print(request.POST)
                products = json.loads(request.POST['products'])
                ordentrabajo = Ordendetrabajo()
                ordentrabajo.fecha = request.POST['fecha']
                ordentrabajo.estado_id = request.POST['estado']
                ordentrabajo.cliente_id = request.POST['cliente']
                ordentrabajo.empleado_id = (request.POST['empleado'])
                ordentrabajo.definicion = request.POST['definicion']
            
                ordentrabajo.save()
                for i in products:
                    det = Detordentrabajo()
                    det.ordendetrabajo_id = ordentrabajo.id
                    det.articulo_id = i['id']
                    det.cant = int(i['cant'])
                    det.save()
                    det.articulo.stock+=det.cant
                    det.articulo.save()
            
                 
            else:
                data['error'] = 'Ha ocurrido un error'

        except Exception as e:
                data['error'] = str(e)
        return JsonResponse(data, safe=False) # para serializarlos cuando es coleccion de elemento ponemos false

    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Crear una orden de trabajo'
        context['entity'] = 'orden de trabajo' #titulo de la tabla y pestaña
        context['action'] = 'add'
        return context 
        #los decoradores pueden modificar de una forma dinamica una funcion


class ordentrabajoUpdateView(UpdateView):
    model = Ordendetrabajo #aqui llamo a mi modelo
    form_class = ordendetrabajoForm #aqui llamo a mi form de fomrs.py
    template_name = 'orden_trabajo/crearregistro.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('ordentrabajolistado') #direccion hacia donde voy a redireccionar
    @method_decorator(permission_required('AppFerrus.change_ordendetrabajo')) 
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            print(request.POST)
            if action == 'search_articulo': #la variable de mi form js
                data = [] #esto porque es un array
                articulos = Articulo.objects.filter(nombre__icontains=request.POST['variablebusqueda'])[0:10] #limitante de mostrar
                for i in articulos:
                    print(i.nombre)
                    item = i.toJSON() #aqui llamo a mi json de mis modelos
                    item['value'] = i.nombre #esto me retornara lo que busco
                    data.append(item) #item es lo que va tirar la busqueda
            elif action == 'searchdetails_prod':
                data= []
                for i in Detordentrabajo.objects.filter(ordendetrabajo_id=request.POST['id']):
                    data.append(i.toJSON())

            elif action == 'edit': #para añadir mi registro
                print(request.POST)
                with transaction.atomic():
                    products = json.loads(request.POST['products'])
                ordentrabajo = Ordendetrabajo()
                ordentrabajo.fecha = request.POST['fecha']
                ordentrabajo.estado_id = request.POST['estado']
                ordentrabajo.cliente_id = request.POST['cliente']
                ordentrabajo.empleado_id = (request.POST['empleado'])
                ordentrabajo.definicion = request.POST['definicion']
                 # para eliminar los detalles de la informacion anterior
                ordentrabajo.save()
                ordentrabajo.detordentrabajo_set.all().delete()
                for i in products:
                    det = Detordentrabajo()
                    det.ordendetrabajo_id = ordentrabajo.id
                    det.articulo_id = i['id']
                    det.cant = int(i['cant'])
                    det.save()
                    det.articulo.stock+=det.cant
                    det.articulo.save()
            
                 
            else:
                data['error'] = 'Ha ocurrido un error'

        except Exception as e:
                data['error'] = str(e)
        return JsonResponse(data, safe=False) # para serializarlos cuando es coleccion de elemento ponemos false

    def get_articulo_detalles(self): #para llamar mis productos
        data = [] #lo hago diccionario
        try:
            for i in Detordentrabajo.objects.filter(ordendetrabajo_id=self.get_object().id):
                item = i.articulo.toJSON() #aqui pido mis articulos
                item['cant'] = i.cant #aqui pido mi cantidad
                data.append(item) #aqui llamo al diccionario
        except: 
            pass
        return data
        
    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Editar orden de trabajo'
        context['entity'] = 'Ordenes de trabajo' #titulo de la tabla y pestaña
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_articulo_detalles(), default=str) # para convetir string
        return context 






class trabajoUpdateView(UpdateView):
    model = Ordendetrabajo #aqui llamo a mi modelo
    form_class = ordendetrabajoForm #aqui llamo a mi form de fomrs.py
    template_name = 'orden_trabajo/editar.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('ordentrabajolistado') #direccion hacia donde voy a redireccionar
    
    @method_decorator(permission_required('AppFerrus.change_venta'))
    def dispatch(self, request, *args, **kwargs): 
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Edicion'
        context['crear_url'] =  reverse_lazy('ordentrabajocrear')
        return context 






class ordentrabajoPdfView(View):
    def link_callback(uri, rel): #para llamar archivos estaticos
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path
    
    
    
    
    
    def get(self, request, *args, **kwargs):
        try:
            template = get_template('orden_trabajo/pdf.html') #aqui obtiene la ruta de la plantilla
            context = {'ordentrabajo': Ordendetrabajo.objects.get(pk=self.kwargs['pk']),
            'comp':{'nombre': 'Multiservicios Agroindustriales Ferrus', 'direccion':'San Jose Pinula Km. 20'}
            } # mi diccionario
            html = template.render(context) #rerenderizar mi diccionario
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="report.pdf"' # mi respuesta para descargar
            pisaStatus = pisa.CreatePDF( #funcion para crear pdf
            html, dest=response, #objeto que va tener el response
            link_callback=self.link_callback
            )
            return response
        except: 
            pass
        return HttpResponseRedirect(reverse_lazy('personalista')) #en caso de erro me retorna a esta pagina

