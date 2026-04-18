from django.test import TestCase

from applications.departamento.models import Departamento
from applications.empleado.models import Empleado, Habilidades, Trabajo


class EmpleadoModelsTest(TestCase):
    def setUp(self):
        self.departamento = Departamento.objects.create(name="Ventas", short_name="VT")
        self.trabajo = Trabajo.objects.create(puesto="Cajero", sueldo=200.00)
        self.habilidad = Habilidades.objects.create(habilidad="Atencion al cliente")

    def test_empleado_full_name_y_str(self):
        empleado = Empleado.objects.create(
            first_name="Juan",
            last_name="Perez",
            job=self.trabajo,
            departamento=self.departamento,
            hoja_vida="Experiencia previa.",
        )
        empleado.habilidades.add(self.habilidad)

        self.assertEqual(empleado.full_name, "Juan Perez")
        self.assertIn("Juan", str(empleado))
        self.assertEqual(empleado.habilidades.count(), 1)
