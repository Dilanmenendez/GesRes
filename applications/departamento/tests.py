from django.db import IntegrityError
from django.test import TestCase

from applications.departamento.models import Departamento


class DepartamentoModelsTest(TestCase):
    def test_departamento_str(self):
        departamento = Departamento.objects.create(name="Administracion", short_name="ADM")
        self.assertEqual(str(departamento), "Administracion")

    def test_departamento_unique_together(self):
        Departamento.objects.create(name="Recursos Humanos", short_name="RRHH")
        with self.assertRaises(IntegrityError):
            Departamento.objects.create(name="Recursos Humanos", short_name="RRHH")
