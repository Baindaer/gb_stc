from django.conf.urls import url

from . import views


app_name = 'stc'
urlpatterns = [
  url(r'^$', views.inicio, name='inicio'),
  url(r'^login/$', views.login, name='login'),
  url(r'^logout/$', views.logout, name='logout'),
  url(r'^radicacion/$', views.radicacion, name='radicacion'),
  url(r'^radicacion/gestion/$', views.gestion_radicacion, name='gestion_radicacion'),
  url(r'^consulta/$', views.consulta, name='consulta'),
  url(r'^reportes/$', views.reportes, name='reportes'),
  url(r'^reportes/capitas$', views.reporte_capitas, name='reporte_capitas'),
  url(r'^devoluciones/$', views.devoluciones, name='devoluciones'),
  url(r'^devoluciones/gestion/$', views.gestion_devoluciones, name='gestion_devoluciones'),
  url(r'^exportar/$', views.exportar, name='exportar'),
  url(r'^reportes/exp_rad_general/$', views.exp_rad_general, name='exp_rad_general'),
  url(r'^pruebas/$', views.pruebas, name='pruebas'),
  url(r'^devoluciones/remision$', views.remision_devoluciones, name='remision_devoluciones'),
  url(r'^devoluciones/actualizacion$', views.dev_actualizacion, name='dev_actualizacion'),
]