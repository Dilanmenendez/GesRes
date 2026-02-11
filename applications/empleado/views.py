from django.contrib import messages
from django.shortcuts import redirect
from .models import Empleado, Habilidades, Trabajo
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView, ListView, DetailView
from django.urls import reverse_lazy
#Importame los forms por favor te lo pido
from .forms import  EmpleadoForm, HabilidadesForm, TrabajoForm
# Create your views here.



class SuccessView(TemplateView):
    template_name = 'persona/success.html'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

#------------ VIEWS EMPLEADO ----------------------------#

class EmpleadoCreateView(CreateView):
    model = Empleado
    template_name = "persona/add.html"
    form_class = EmpleadoForm
    success_url = reverse_lazy('persona_app:correcto')

    #def form_valid(self, form):
        #Logica del proceso
        #Con commit=False lo que haces es crear la instancia que se va a guardar durante el proceso
        #Pero aun no la guarda, osea te permite utilizar dicha instancia, pero no la guarda instantaneamente

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["habilidades"] = Habilidades.objects.all()
        
        return context

class EmpleadoUpdateView(UpdateView):
    model = Empleado
    template_name = 'persona/update.html'

    form_class = EmpleadoForm
    success_url = reverse_lazy('persona_app:correcto')


class EmpleadoDeleteView(DeleteView):
    model = Empleado
    template_name = "persona/delete.html"
    success_url = reverse_lazy('persona_app:correcto')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        nombre = self.object.first_name
        messages.success(
            request, f"El empleado {nombre} fue eliminado")

        return super().post(request, *args, **kwargs)


class ListAllEmpleado(ListView):
    model = Empleado
    template_name = "persona/list_all.html"
    paginate_by = 4

    def get_queryset(self):
        pk_id = self.request.GET.get('id', '')
        palabra_clave = self.request.GET.get("kword", '')
        if pk_id:
            return Empleado.objects.buscar_empleado_id(pk_id)
        
        return Empleado.objects.buscar_empleado(palabra_clave)
         
class EmpleadoDetailView(DetailView):
    model = Empleado
    template_name = "persona/by_kword.html"
    context_object_name = "empleado"


class EmpleadoByAreaListView(ListView):
    template_name = "persona/list_byarea.html"

    def get_queryset(self):
        area = self.kwargs['name']
        return Empleado.objects.buscar_by_area(area)

class EmpleadoByTrabajoListView(ListView):
    template_name = "persona/list_bytrabajo.html"

    def get_queryset(self):
        area = self.kwargs['puesto']
        return Empleado.objects.buscar_by_trabajo(area)

#-------------------- TRABAJO VIEWS ----------------------#

class CrearTrabajoView(CreateView):
    model = Trabajo
    form_class = TrabajoForm
    template_name = 'persona/crear_trabajo.html'
    success_url = reverse_lazy('persona_app:correcto')

class ListAllTrabajos(ListView):
    model = Trabajo
    template_name = "persona/list_all_trabajos.html"
    paginate_by = 4

    def get_queryset(self):
        palabra_clave = self.request.GET.get("kword", '')
        pk_id = self.request.GET.get('id', '')
        if pk_id:
            return Trabajo.objects.buscar_trabajo_id(pk_id)
        
        return Trabajo.objects.buscar_trabajo(palabra_clave)

class TrabajoDeleteView(DeleteView):
    model = Trabajo
    template_name = "persona/delete_trabajo.html"
    success_url = reverse_lazy('persona_app:correcto')

class TrabajoUpdateView(UpdateView):
    model = Trabajo
    template_name = "persona/update_trabajo.html"
    success_url = reverse_lazy('persona_app:correcto')
    form_class = TrabajoForm

#------------------ OTRAS VIEWS -------------------#
class InicioView(TemplateView):
    template_name = "inicio.html"

class EmpleadoDashboardView(TemplateView):
    template_name = "persona/dashboard.html"


class CrearHabilidadView(CreateView):
    model = Habilidades
    form_class = HabilidadesForm
    template_name = "persona/crear_habilidad.html"

    def get_success_url(self):
        return (
            self.request.POST.get("next")
            or self.request.GET.get("next")
            or reverse_lazy("persona_app:add_empleado")
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = (
            self.request.GET.get("next")
            or self.request.META.get("HTTP_REFERER")
        )
        return context

