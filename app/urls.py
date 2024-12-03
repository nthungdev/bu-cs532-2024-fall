from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('query/<int:query_index>', views.query, name='query'),
]