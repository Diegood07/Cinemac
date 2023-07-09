from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('panel_administracion/',views.index,name="panel_administracion"),
    path('administradores/administradores_totales/',views.admins_totales,name="admins_totales"),
    path('administradores/crear_administrador/',views.crear_admin,name="crear_admin"),
    path('administradores/modificar_administrador/',views.modificar_administrador,name="modificar_admin"),
    path('administradores/opciones_administradores/',views.opc_admins,name="opciones_administrador"),
    path('administradores/encontrar_administrador/<str:pk>',views.encontrar_administrador,name="encontrar_administrador"),
    path('administradores/eliminar_administrador/<str:pk>',views.eliminar_administrador,name="eliminar_administrador"),
    path('Imagenes/imagenes_totales/',views.imagenes_totales,name="imagenes_totales"),
    path('Imagenes/subir_imagen/',views.subir_imagen,name="subir_imagen"),
    path('Imagenes/modificar_imagen/',views.modificar_imagen,name="modificar_imagen"),
    path('Imagenes/opciones_imagenes/',views.opciones_imagen,name="opciones_imagenes"),
    path('Imagenes/encontrar_imagen/<str:pk>',views.encontrar_imagen,name="encontrar_imagen"),
    path('Imagenes/eliminar_imagen/<str:pk>',views.eliminar_imagen,name="eliminar_imagen"),
    path('peliculas/peliculas_totales/',views.peliculas_totales,name="peliculas_totales"),
    path('peliculas/crear_pelicula/',views.crear_pelicula,name="crear_pelicula"),
    path('peliculas/modificar_pelicula/',views.modificar_pelicula,name="modificar_pelicula"),
    path('peliculas/opciones_peliculas/',views.opciones_peliculas,name="opciones_peliculas"),
    path('peliculas/encontrar_pelicula/<str:pk>',views.encontrar_pelicula,name="encontrar_pelicula"),
    path('peliculas/eliminar_pelicula/<str:pk>',views.eliminar_pelicula,name="eliminar_pelicula"),
    path('usuarios/usuarios_totales/',views.usuarios_totales,name="usuarios_totales"),
    path('usuarios/crear_usuario/',views.crear_usuario,name="crear_usuario"),
    path('usuarios/modificar_usuario/',views.modificar_usuario,name="modificar_usuario"),
    path('usuarios/opciones_usuarios/',views.opciones_usuarios,name="opciones_usuarios"),
    path('usuarios/encontrar_usuario/<str:pk>',views.encontrar_usuario,name="encontrar_usuario"),
    path('usuarios/eliminar_usuario/<str:pk>',views.eliminar_usuario,name="eliminar_usuario")
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)