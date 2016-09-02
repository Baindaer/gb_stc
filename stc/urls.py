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

]