from django.db import models

# Create your models here.

class Peliculas(models.Model):
    id_pelicula = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=30,null=False)
    precio = models.IntegerField(null=False)
    imagen = models.ImageField(null=False)

    def __str__(self):
        return self.titulo

class Imagen(models.Model):
    id_imagen = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=30,null=False)
    imagen = models.ImageField()
    descripcion_imagen = models.CharField(max_length=70,null=True)

class Administradores(models.Model):
    id_admin = models.AutoField(primary_key=True)
    nombre_admin = models.CharField(max_length=40, null=False)
    contrasena_admin = models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.nombre_admin