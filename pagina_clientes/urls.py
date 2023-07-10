from django.urls import path
from . import views

urlpatterns = [
    path('',views.inicio,name='inicio'),
    path('html/login/',views.login,name='login'),
    path('html/cartelera/',views.cartelera,name='cartelera'),
    path('html/index/',views.index, name="index"),
    path('html/Lomasvisto/',views.mas_visto,name='mas_visto'),
    path('html/preventas/',views.preventas,name='preventas'),
    path('html/signup/',views.signup,name='signup'),
    path('html/inicio/',views.inicio,name='inicio'),
    path('html/formulario/',views.formulario,name='formulario'),
]