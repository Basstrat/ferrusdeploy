from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from AppFerrus.models import Cotizacion
from AppFerrus.forms import CotizacionForm
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.db import transaction
from django.contrib.auth.decorators import permission_required
from AppFerrus.models import Articulo
from AppFerrus.models import Detcotizacion

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string


#from weasyprint.fonts import FontConfiguration

#librerias para pdf
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders



class Cotizacionlistview(ListView):
    model = Cotizacion
    template_name = 'cotizacion/lista.html' # este es el que uso para mi listado

    @method_decorator(permission_required('AppFerrus.view_cotizacion')) 
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = [] #es una array
                for i in Cotizacion.objects.all():
                    data.append(i.toJSON()) #incrustar datos dentro del array
            elif action == 'search_details_prod':
                data = []
                for i in Detcotizacion.objects.filter(cotizacion_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False) #safe= false para que maneje varios datos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado cotizacion'
        context['entity'] = 'Cotizacion'
        context['create_url'] = reverse_lazy('cotizacioncrear')
        context['list_url'] = reverse_lazy('cotizacionlistado')
        return context
    #vista basada en clases








#este es para mi formulario

class CotizacionCreateView(CreateView):
    model = Cotizacion #aqui llamo a mi modelo
    form_class = CotizacionForm #aqui llamo a mi form de fomrs.py
    template_name = 'cotizacion/crearregistro.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('cotizacionlistado') #direccion hacia donde voy a redireccionar
    
    #aqui viy a definir para cuando se aguarde un dato repetido
    @method_decorator(permission_required('AppFerrus.add_cotizacion'))
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
                for i in Detcotizacion.objects.filter(cotizacion_id=request.POST['id']):
                    data.append(i.toJSON())

            elif action == 'add': #para añadir mi registro
                print(request.POST)
                cotizacion1 = json.loads(request.POST['cotizacion1'])
                cotizacion = Cotizacion()
                cotizacion.fecha = cotizacion1['fecha']
                cotizacion.cliente_id = cotizacion1['cliente']
                cotizacion.subtotal = float(cotizacion1['subtotal'])
                cotizacion.total = float(cotizacion1['total'])
                cotizacion.porciento = float(cotizacion1['porciento'])
                cotizacion.terminos = cotizacion1['terminos']
                cotizacion.save()
                
    #iterar productos
                for i in cotizacion1['articulo']:
                    det = Detcotizacion()
                    det.cotizacion_id = cotizacion.id
                    det.articulo_id = i['id']
                    det.cant = int(i['cant'])
                    det.precio = float(i['precio'])
                    det.subtotal = float(i['subtotal'])
                    det.save()
                
                    
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
                data['error'] = str(e)
        return JsonResponse(data, safe=False) # para serializarlos cuando es coleccion de elemento ponemos false

    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Crear una Cotizacion'
        context['entity'] = 'Cotizaciones' #titulo de la tabla y pestaña
        context['action'] = 'add'
        context['det'] = []
        return context 
        #los decoradores pueden modificar de una forma dinamica una funcion


class cotizacionUpdateView(UpdateView):
    model = Cotizacion #aqui llamo a mi modelo
    form_class = CotizacionForm #aqui llamo a mi form de fomrs.py
    template_name = 'cotizacion/crearregistro.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('cotizacionlistado') #direccion hacia donde voy a redireccionar
    
    @method_decorator(permission_required('AppFerrus.change_cotizacion')) 
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
                for i in Detcotizacion.objects.filter(Cotizacion_id=request.POST['id']):
                    data.append(i.toJSON())

            elif action == 'edit': #para añadir mi registro
                print(request.POST)
                with transaction.atomic():
                    cotizacion1 = json.loads(request.POST['cotizacion1'])
                #cotizacion = Cotizacion.objects.gets(pk=self.get().id)
                    cotizacion = self.get_object() #me devuele la instancia de los que estoy editando
                    cotizacion.fecha = cotizacion1['fecha']
                    cotizacion.cliente_id = cotizacion1['cliente']
                    cotizacion.subtotal = float(cotizacion1['subtotal'])
                    cotizacion.total = float(cotizacion1['total'])
                    cotizacion.porciento = float(cotizacion1['porciento'])
                    cotizacion.terminos = cotizacion1['terminos']
                    cotizacion.save()
                    cotizacion.detcotizacion_set.all().delete() # para eliminar los detalles de la informacion anterior
                
    #iterar productos
                for i in cotizacion1['articulo']:
                    det = Detcotizacion()
                    det.cotizacion_id = cotizacion.id
                    det.articulo_id = i['id']
                    det.cant = int(i['cant'])
                    det.precio = float(i['precio'])
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
            for i in Detcotizacion.objects.filter(cotizacion_id=self.get_object().id):
                item = i.articulo.toJSON() #aqui pido mis articulos
                item['cant'] = i.cant #aqui pido mi cantidad
                data.append(item) #aqui llamo al diccionario
        except: 
            pass
        return data
        
    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Crear una Cotizacion'
        context['entity'] = 'Cotizaciones' #titulo de la tabla y pestaña
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_articulo_detalles(), default=str) # para convetir string
        return context 

class cotizacionDeleteView(DeleteView):
    model = Cotizacion #aqui llamo a mi modelo
    template_name = 'cotizacion/eliminaregistro.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('cotizacionlistado') #direccion hacia donde voy a redireccionar
    
    @method_decorator(permission_required('AppFerrus.delete_cotizacion'))
    def dispatch(self, request, *args, **kwargs): 
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion'
        context['crear_url'] =  reverse_lazy('eliminaregistro')
        context['lista_url'] = self.success_url
        return context 



class cotizacionPdfView(View):
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
            template = get_template('cotizacion/pdf.html') #aqui obtiene la ruta de la plantilla
            context = {'cotizacion': Cotizacion.objects.get(pk=self.kwargs['pk']),
            'comp':{'nombre': 'Multiservicios Agroindustriales Ferrus', 'direccion':'San Jose Pinula Km. 20'},
            'icono': '{}{}'.format(settings.STATICFILES_DIRS, 'img/ferrus.jpg')
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

