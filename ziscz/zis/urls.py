# coding=utf-8
import loginas.urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.views.decorators.cache import cache_page
from django_js_reverse.views import urls_js

urlpatterns = [
                  path('i18n/', include('django.conf.urls.i18n')),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('admin/', include(loginas.urls)),
                  path('admin/', admin.site.urls),
                  path('select2-api/', include('django_select2.urls')),
                  path('api/', include('ziscz.api.urls')),
                  path('js-reverse', cache_page(3600)(urls_js), name='js_reverse'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
                  path('', include('ziscz.web.urls'))
              ] + staticfiles_urlpatterns()
