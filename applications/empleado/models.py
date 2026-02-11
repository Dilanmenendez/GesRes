from django.db import models
from ckeditor.fields import RichTextField
from applications.departamento.models import Departamento
from django.core.validators import FileExtensionValidator
from .managers import EmpleadoManager, TrabajoManager

class Habilidades(models.Model):
    """Model definition for Habilidades."""
    habilidad = models.CharField('Habilidad', 
                                 max_length=50)
    # TODO: Define fields here

    class Meta:
        """Meta definition for Habilidades."""

        verbose_name = 'Habilidades'
        verbose_name_plural = 'Habilidadess'

    def __str__(self):
        """Unicode representation of Habilidades."""
        return f'{self.habilidad}'


class Trabajo(models.Model):
    puesto = models.CharField('Puesto', 
                              max_length=50)
    sueldo = models.DecimalField('Sueldo', 
                                 max_digits=7, 
                                 decimal_places=2)
    objects = TrabajoManager()
    
    class Meta:
        verbose_name = 'Puesto de Trabajo'
        verbose_name_plural = 'Puestos de Trabajo'
        ordering = ['puesto']

    def __str__(self):
        return self.puesto

# Create your models here.
class Empleado(models.Model):
    first_name = models.CharField('Nombre', 
                                  max_length=50)
    last_name = models.CharField('Apellidos', 
                                 max_length=50)
    job = models.ForeignKey(Trabajo, 
                            on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamento, 
                                     on_delete=models.CASCADE)
    #image = models.ImageField(, upload_to=None, height_field=None, width_field=None, max_length=None)
    habilidades = models.ManyToManyField(Habilidades, 
                                         blank=True)
    hoja_vida = RichTextField()
    cv = models.FileField(upload_to='pdfs/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        null=True, blank=True)
    objects = EmpleadoManager()

    class Meta:
        verbose_name = 'Empleados'
        verbose_name_plural = 'Lista Empleados'
        ordering = ['first_name']
        unique_together = ('first_name', 'last_name')

    def __str__(self):
        return f'{self.first_name} | {self.last_name} | {self.job} | {self.departamento} | {self.id}'
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'