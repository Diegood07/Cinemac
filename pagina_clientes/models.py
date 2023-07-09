from django.db import models

# Create your models here.

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    correo_usuario = models.CharField(max_length=50, null=False)
    contrasena_usuario = models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.nombre_usuario + ' - ' + self.correo_usuario