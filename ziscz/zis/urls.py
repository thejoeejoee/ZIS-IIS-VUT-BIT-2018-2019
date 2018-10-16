# coding=utf-8
import loginas.urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

urlpatterns = [
                  path('i18n/', include('django.conf.urls.i18n')),
                  path('admin/', include(loginas.urls)),
                  path('admin/', admin.site.urls),
                  path('select2-api/', include('django_select2.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
                  path('', include('ziscz.web.urls'))
              ] + staticfiles_urlpatterns()
