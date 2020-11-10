from django.conf.urls import include, url
from django.contrib import admin
from dentalE.views import ingreso, logout_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', ingreso, name='ingreso'),
    url(r'^dentalE/', include('dentalE.urls')),
    url(r'^logout', logout_view, name='logout'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^media/', include('gridfs_storage.urls')),

]
