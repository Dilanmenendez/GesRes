from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .forms import NewDepartamentoForm, CreateDepartamentoForm, DepartamentoUpdateForm
from django.urls import reverse_lazy
from applications.empleado.models import Empleado
from .models import Departamento

# Create your views here.
#El FormView nos va a servir cuando necesitemos procesar datos para diferentes tablas,
#En un mismo template
class NewDepartamentoView(FormView):
    template_name = 'departamento/new_departamento.html'
    form_class = NewDepartamentoForm
    success_url = reverse_lazy('persona_app:correcto')

    def form_valid(self, form):
        print(f'Estamos en el form valid')

        depa = Departamento(
            name = form.cleaned_data['departamento'],
            short_name = form.cleaned_data['short_name']
        )
        #hasta aqui eso no se guardo en la base de datos, pero eso lo arreglamos facilito asi:
        depa.save()

        #El form que recuperaos aqui,  es que form que hicimos en forms.py, el cual es un diccionario
        #con cleaned data accedemos a los datos dle diccionario, y luego especificamos cual queremos
        nombre = form.cleaned_data['nombre']
        apellido = form.cleaned_data['apellido']
        #Para crear el empleado con la clase Empleado, usamos el orm de django y objects.create
        #cuando usamos object.create, no necesitamos hacer .save() porque lo hace automaticamente
        Empleado.objects.create(
            first_name = nombre,
            last_name = apellido,
            job = '1', #Le ponemos uno por defecto
            #y le pasamos depa como valor al atributo departamento de Empleado
            departamento = depa
        )
        return super(NewDepartamentoView, self).form_valid(form)


class DepartamentoListAllView(ListView):
    model = Departamento
    template_name = "departamento/list_all.html"
    ordering = 'name'
    paginate_by = 4

    def get_queryset(self):
        palabra_clave = self.request.GET.get("kword", '')
        lista = Departamento.objects.filter(
            name__icontains = palabra_clave
        ) 
        #icontains nos ahorra toda la logica de si no hay empleados con ese nombre, o al principio que no nos muestra nada
        #icontains nos ahorra todo eso, django lo hace automatico
        #lo que hace es buscar la palabra clave dentro de toda la cadena (en este caso first_name)
        return lista


class DepartamentoCreateView(CreateView):
    model = Departamento
    template_name = "departamento/create_departamento.html"
    form_class = CreateDepartamentoForm
    success_url = reverse_lazy('persona_app:correcto')

class DepartamentoDeleteView(DeleteView):
    model = Departamento
    template_name = "departamento/delete_departamento.html"
    success_url = reverse_lazy('persona_app:correcto')


class DepartamentoUpdateView(UpdateView):
    model = Departamento
    template_name = "departamento/update_departamento.html"
    form_class = DepartamentoUpdateForm
    success_url = reverse_lazy('persona_app:correcto')