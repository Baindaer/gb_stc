from django.conf.urls import url

from . import views


app_name = 'stc'
urlpatterns = [
  url(r'^$', views.inicio, name='inicio'),
  url(r'^login/$', views.login, name='login'),
  url(r'^logout/$', views.logout, name='logout'),
  url(r'^radicacion/$', views.radicacion, name='radicacion'),
  url(r'^radicacion/agregar/$', views.rad_agregar, name='rad_agregar'),
  url(r'^radicacion/gestion/$', views.rad_gestion, name='rad_gestion'),
  url(r'^consulta/$', views.consulta, name='consulta'),
  url(r'^reportes/$', views.reportes, name='reportes'),
  url(r'^reportes/capitas$', views.rep_capitas, name='rep_capitas'),
  url(r'^devoluciones/$', views.devoluciones, name='devoluciones'),
  url(r'^devoluciones/gestion/$', views.dev_gestion, name='dev_gestion'),
  url(r'^exportar/$', views.exportar, name='exportar'),
  url(r'^reportes/exp_rad_general/$', views.exp_rad_general, name='exp_rad_general'),
  url(r'^pruebas/$', views.pruebas, name='pruebas'),
  url(r'^devoluciones/remision$', views.dev_remision, name='dev_remision'),
  url(r'^devoluciones/actualizacion$', views.dev_actualizacion, name='dev_actualizacion'),
  url(r'^devoluciones/agregar$', views.dev_agregar, name='dev_agregar'),
]