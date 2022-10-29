# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True, unique=True
#   * Make sure each OneToOneField and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from datetime import datetime

from django.forms import model_to_dict
from django.contrib.auth.models import AbstractBaseUser, AbstractUser #donde va ehredar mi modelos usuario
from django.contrib.auth.models import BaseUserManager, PermissionsMixin #la bases para crear un model usuario       





class EstadoOrdentrabajo(models.Model):
    idordentrabajo = models.IntegerField(primary_key=True, unique=True)
    estado = models.CharField(max_length=45, blank=True, null=True)
    def __str__(self): #como van a salir en mis vistas
        return self.estado
    
    def toJSON(self):
        item = model_to_dict(self)
        return item
    class Meta:
        verbose_name = 'EstadoOrdentrabajo'
        verbose_name_plural = 'EstadoOrdentrabajos'
        ordering = ['idordentrabajo']




      

class Material(models.Model):
    nombre = models.CharField(max_length=45, blank=True, null=True, unique=True)
    descripcion = models.CharField(max_length=45, blank=True, null=True)
    stock = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    totalcompra = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantidadcompra = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    precio_unidad = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self): #como van a salir en mis vistas
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self) #para hacerlos diccionario
        item['precio_unidad'] = float(self.precio_unidad)
        item['stock'] = float(self.precio_unidad)
        return item
  

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiales'
        ordering = ['id']

class Articulo(models.Model):
    fecha = models.DateField(default=datetime.now)
    nombre = models.CharField(max_length=45, blank=False, null=True, unique=True)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    descripcion = models.CharField(max_length=45, blank=True, null=True)
    mano_de_obra = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    otrosgastos = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    porciento = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    stock = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    stockenviado = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        #item['idarticulo'] = format(self.idarticulo, '.2f')
        item['precio'] = float(self.precio)
        item['mano_de_obra'] = float(self.mano_de_obra) 
        item['otrosgastos'] = float(self.otrosgastos)
        item['subtotal'] = float(self.subtotal)
        item['porciento'] = float(self.porciento)
        item['det'] = [i.toJSON() for i in self.detarticulo_set.all()]
        return item

    class Meta:
       verbose_name = 'Articulo'
       verbose_name_plural = 'Articulos'
       ordering = ['id']


class Detarticulo(models.Model):
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.material.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['articulo'])
        item['material'] = self.material.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle articulo'
        verbose_name_plural = 'Detalle articulos'
        ordering = ['id']



       
class Cliente(models.Model):
    nombre = models.CharField(max_length=45, blank=False, null=True, unique=True )
    descripcion = models.CharField(max_length=45, blank=True, null=True)
    direccion = models.CharField(max_length=45, blank=True, null=True)
    telefono = models.CharField(max_length=45, blank=True, null=True)
    nit = models.FloatField(max_length=10, blank=True, null=True)  # Field name made lowercase.
    
    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']
       
        


class Cotizacion(models.Model):
    terminos = models.CharField(max_length=45, blank=True, null=True)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    porciento = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    fecha = models.DateField(default=datetime.now)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.cliente.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        item['cliente'] = self.cliente.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['total'] = format(self.total, '.2f')
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detcotizacion_set.all()] #para obtener relaciones con llave foreana
        return item

    class Meta:
        verbose_name = 'Cotizacion'
        verbose_name_plural = 'Cotizaciones'
        ordering = ['id']
       
class Detcotizacion(models.Model):
        
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.articulo.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['cotizacion'])
        item['articulo'] = self.articulo.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle cotizacion'
        verbose_name_plural = 'Detalle cotizaciones'
        ordering = ['id']

class Proveedores(models.Model):
    nombre = models.CharField(max_length=45, blank=False, null=True, unique=True)
    direccion = models.CharField(max_length=45, blank=True, null=True)
    telefono = models.IntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=45, blank=True, null=True)
    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['id']

class OrdenCompraMaterial(models.Model):
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    observaciones = models.CharField(max_length=45, blank=True, null=True)
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, default=0)
    fecha = models.DateField(default=datetime.now, verbose_name='Fecha_venta')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantidadcompra = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.proveedor.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        item['articulo'] = self.articulo.toJSON()
        item['proveedor'] = self.proveedor.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['total'] = format(self.total, '.2f')
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detordencompra_set.all()] #para obtener relaciones con llave foreana
        return item



    class Meta:
        verbose_name = 'OrdenCompraMaterial'
        verbose_name_plural = 'OrdenCompraMateriales'
        ordering = ['id']
     
class DetOrdenCompra(models.Model):
        
    orden_compra_material = models.ForeignKey(OrdenCompraMaterial, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, default=0)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.CharField(max_length=45, blank=True, null=True)
    stock = models.IntegerField(default=0)
    totalcompra = models.IntegerField(default=0)
    cantidadcompra = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['idorden_compra_material'])
        item['material'] = self.material.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        item['stock'] = format(self.stock, '.2f')
        item['cantidadcompra'] = format(self.cantidadcompra, '.2f')
        item['totalcompra'] = format(self.totalcompra, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle cotizacion'
        verbose_name_plural = 'Detalle cotizaciones'
        ordering = ['id']


    

class Persona(models.Model):
    nombre = models.CharField(max_length=45, blank=False, null=True)
    apellido = models.CharField(max_length=45, blank=True, null=True)
    direccion = models.CharField(max_length=45, blank=True, null=True)
    telefono = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        return item
    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        ordering = ['id']


class Puestoempleado(models.Model):
    nombre = models.CharField(max_length=45, blank=False, null=True)
    descripcion = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = 'Puestoempleado'
        verbose_name_plural = 'Puestoempleados'
        ordering = ['id']

class Empleado(models.Model):
    persona = models.OneToOneField(Persona,  default=0, on_delete=models.CASCADE, related_name='empleadopersona')
    puestoempleado = models.OneToOneField(Puestoempleado, on_delete=models.CASCADE, default=0, related_name='empleadopuesto')
    sueldo = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    def __str__(self):
        return self.persona.nombre
    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['id']




     

class EstadoVenta(models.Model):
    estado = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return self.estado
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'EstadoVenta'
        verbose_name_plural = 'EstadoVentas'
        ordering = ['id']
     



class Venta(models.Model):
    fecha = models.DateField(default=datetime.now, verbose_name='Fecha_venta')
    estado = models.ForeignKey(EstadoVenta, on_delete=models.CASCADE, default=0)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    
    def toJSON(self):
        item = model_to_dict(self)
        item['cliente'] = self.cliente.toJSON()
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        item['estado'] = self.estado.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['total'] = format(self.total, '.2f')
        item['det'] = [i.toJSON() for i in self.detventa_set.all()]
        return item
    
    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']

class Detventa(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.articulo.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['venta'])
        item['articulo'] = self.articulo.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle Venta'
        verbose_name_plural = 'Detalle Ventas'
        ordering = ['id']
             
class Ordendetrabajo(models.Model):
    definicion = models.CharField(max_length=45, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE,  default=0)
    estado = models.ForeignKey(EstadoOrdentrabajo, on_delete=models.CASCADE,  default=0)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.cliente.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['empleado'] = self.empleado.toJSON()
        item['cliente'] = self.cliente.toJSON()
        item['estado'] = self.estado.toJSON()
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detordentrabajo_set.all()]
        return item

class Meta:
        verbose_name = 'Orden de trabajo'
        verbose_name_plural = 'Ordenes de trabajos'
        ordering = ['id']

class Detordentrabajo(models.Model):
        
    ordendetrabajo = models.ForeignKey(Ordendetrabajo, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cant = models.IntegerField(default=0)

    def __str__(self):
        return self.articulo.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['ordendetrabajo'])
        item['articulo'] = self.articulo.toJSON()
        return item

    class Meta:
        verbose_name = 'Detalle orden de trabajo'
        verbose_name_plural = 'Detalle ordenes de trabajo'
        ordering = ['id']

#class Usuario(models.Model):
class Envios(models.Model):
    observaciones = models.CharField(db_column='Observaciones', max_length=45, blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateField(default=datetime.now)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=0)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE,  default=0)
    
    def toJSON(self):
        item = model_to_dict(self)
        item['cliente'] = self.cliente.toJSON()
        item['empleado'] = self.empleado.toJSON()
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detenvios_set.all()]
        return item
    
    class Meta:
        verbose_name = 'Envio'
        verbose_name_plural = 'Envios'
        ordering = ['id']
            
class Detenvios(models.Model):
        
    envios = models.ForeignKey(Envios, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cant = models.IntegerField(default=0)

    def __str__(self):
        return self.articulo.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['envios'])
        item['articulo'] = self.articulo.toJSON()
        return item

    class Meta:
        verbose_name = 'Detalle envio'
        verbose_name_plural = 'Detalle envios'
        ordering = ['id']
   
