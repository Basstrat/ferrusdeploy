from django.urls import path




#from .views import myfirstbiew, mysecondview
from .vistas.persona.views import Personalistview, PersonaCreateView, PersonaUpdateView, PersonaDeleteView
from .vistas.cliente.views import Clientelistview, ClienteCreateView, ClienteUpdateView, ClienteDeleteView
from .vistas.proveedor.views import Proveedoreslistview, ProveedoresCreateView, ProveedoresUpdateView, ProveedoresDeleteView

from .vistas.articulo.views import *
from .vistas.material.views import materiallistview, materialCreateView, materialUpdateView, materialDeleteView
from .vistas.cotizacion.views import CotizacionCreateView, Cotizacionlistview, cotizacionDeleteView, cotizacionPdfView, cotizacionUpdateView
from .vistas.orden_compra.views import orden_compraCreateView, orden_compralistview, ordencompraPdfView, ordencompraUpdateView
from .vistas.orden_trabajo.views import *
from .vistas.venta.views import *
from .vistas.envio.views import *

from .vistas.empleado.views import *


urlpatterns = [
    #path('uno/', myfirstbiew, name='vista1'),
    #path('segunda/', mysecondview),
    #persona
    path('empleado/listado/', Empleadolistview.as_view(), name = 'empleadolista' ),
    path('empleado/añadirregistro/', EmpleadoCreateView.as_view(), name = 'empleadoañadirregistro' ),
    path('empleado/editarregistro/<int:pk>/', EmpleadoUpdateView.as_view(), name = 'empleadoeditarregistro' ), #int pk para reconosca que id vamos a editar
    path('empleado/eliminaregistro/<int:pk>/', EmpleadoDeleteView.as_view(), name = 'empleadoeliminar' ),
    #cliente
    path('cliente/listado/', Clientelistview.as_view(), name = 'clientelista' ),
    path('cliente/añadirregistro/', ClienteCreateView.as_view(), name = 'clienteañadirregistro' ),
    path('cliente/editarregistro/<int:pk>/', ClienteUpdateView.as_view(), name = 'clienteeditarregistro' ), #int pk para reconosca que id vamos a editar
    path('cliente/eliminaregistro/<int:pk>/', ClienteDeleteView.as_view(), name = 'clienteeliminaregistro' ),

    #proveedores
    path('proveedor/listado/',  Proveedoreslistview.as_view(), name = 'proveedoreslista' ),
    path('proveedor/añadirregistro/',  ProveedoresCreateView.as_view(), name = 'proveedoresañadirregistro' ),
    path('proveedor/editarregistro/<int:pk>/',  ProveedoresUpdateView.as_view(), name = 'proveedoreseditarregistro' ), #int pk para reconosca que id vamos a editar
    path('proveedor/eliminaregistro/<int:pk>/',  ProveedoresDeleteView.as_view(), name = 'proveedoreseliminaregistro' ),

  #articulo
    path('articulo/listado/',  articulolistview.as_view(), name = 'articulolista' ),
    path('articulo/añadirregistro/',  articuloCreateView.as_view(), name = 'articuloañadirregistro' ),
    path('articulo/eliminaregistro/<int:pk>/',  articuloDeleteView.as_view(), name = 'articuloeliminaregistro' ),
    path('articulo/editarregistro/<int:pk>/',  articuloUpdateView.as_view(), name = 'articuloeditar' ),
    path('articulo/cambio/<int:pk>/',  articulosUpdateView.as_view(), name = 'articulocambio' ),

  #material
    path('material/listado/', materiallistview.as_view(), name = 'materiallista' ),
    path('material/añadirregistro/',  materialCreateView.as_view(), name = 'materialañadirregistro' ),
    path('material/editarregistro/<int:pk>/',  materialUpdateView.as_view(), name = 'materialeditarregistro' ), #int pk para reconosca que id vamos a editar
    path('material/eliminaregistro/<int:pk>/',  materialDeleteView.as_view(), name = 'materialeliminaregistro' ),
 
 #cotizacion
    path('cotizacion/crear/', CotizacionCreateView.as_view(), name = 'cotizacioncrear' ),
    path('cotizacion/listado/', Cotizacionlistview.as_view(), name = 'cotizacionlistado' ),
    path('cotizacion/eliminar/<int:pk>/', cotizacionDeleteView.as_view(), name = 'cotizacioneliminar' ),
    path('cotizacion/editar/<int:pk>/', cotizacionUpdateView.as_view(), name = 'cotizacioneditar' ),
    path('cotizacion/imprimir/<int:pk>/', cotizacionPdfView.as_view(), name = 'cotizacionpdf' ),

    path('orden_compra/crear/<int:pk>/', orden_compraCreateView.as_view(), name = 'ordencompracrear' ),
    path('orden_compra/listado/', orden_compralistview.as_view(), name = 'ordencompralistado' ),
    path('orden_compra/imprimir/<int:pk>/', ordencompraPdfView.as_view(), name = 'ordencomprapdf' ), 
    path('orden_compra/editar/<int:pk>/', ordencompraUpdateView.as_view(), name = 'ordencompraeditar' ),
    
    path('orden_trabajo/crear/', orden_trabajoCreateView.as_view(), name = 'ordentrabajocrear' ),
    path('orden_trabajo/listado/', orden_trabajolistview.as_view(), name = 'ordentrabajolistado' ),
    path('orden_trabajo/eliminar/<int:pk>/', cotizacionDeleteView.as_view(), name = 'cotizacioneliminar' ),
    path('orden_trabajo/imprimir/<int:pk>/', ordentrabajoPdfView.as_view(), name = 'ordentrabajopdf' ),
    path('orden_trabajo/cambiar/<int:pk>/', ordentrabajoUpdateView.as_view(), name = 'ordentrabajocambiar' ),
    path('orden_trabajo/editar/<int:pk>/', trabajoUpdateView.as_view(), name = 'ordentrabajoeditar' ),


    path('venta/crear/', VentaCreateView.as_view(), name = 'ventacrear' ),
    path('venta/listado/', Ventalistview.as_view(), name = 'ventalistado' ),
    path('venta/imprimir/<int:pk>/', ventaPdfView.as_view(), name = 'ventapdf' ),
    path('venta/update/<int:pk>/', ventaUpdateView.as_view(), name = 'ventaupdate' ),
    path('venta/editar/<int:pk>/', ventasUpdateView.as_view(), name = 'ventaeditar' ),    
   #persona
    path('persona/listado/', Personalistview.as_view(), name = 'personalista' ),
    path('persona/añadirregistro/', PersonaCreateView.as_view(), name = 'personaañadirregistro' ),
    path('persona/editarregistro/<int:pk>/', PersonaUpdateView.as_view(), name = 'personaeditarregistro' ), #int pk para reconosca que id vamos a editar
    path('persona/eliminaregistro/<int:pk>/', PersonaDeleteView.as_view(), name = 'eliminaregistro' ),


    #envios
    path('envio/crear/', EnviosCreateView.as_view(), name = 'enviocrear' ),
    path('envio/listado/', Envioslistview.as_view(), name = 'enviolistado' ),
    path('envio/imprimir/<int:pk>/', envioPdfView.as_view(), name = 'enviopdf' ), 
    path('envio/editar/<int:pk>/', envioUpdateView.as_view(), name = 'envioeditar' ),
   #envios
   
]
