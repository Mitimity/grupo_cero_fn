from django.conf.urls import url
from rest_framework import urlpatterns
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^api/obras/$',views.ObraViewSet.as_view()),
    url(r'^api/tecnica/$',views.TecnicaViewSet.as_view()),
    url(r'^api/buscar_obra/(?P<nombre>.+)/$',views.BuscarObraViewSet.as_view()),
]
urlpatterns=format_suffix_patterns(urlpatterns)
