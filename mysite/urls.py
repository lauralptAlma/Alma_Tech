from django.conf.urls import include, url
from django.contrib import admin
from dentalE.views import ingreso

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', ingreso, name='ingreso'),
    url(r'^dentalE/', include('dentalE.urls')),

]