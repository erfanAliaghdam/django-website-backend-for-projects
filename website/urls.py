from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
import private_storage.urls



urlpatterns = [
    path('__debug__/',                include('debug_toolbar.urls')),
    path("admin/",                    admin.site.urls),
    path('',                          include('core.urls'), name='core'),
    path('api/',                      include('web.urls'), name='web'),
    re_path('^private-media/',        include(private_storage.urls)),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# urlpatterns += i18n_patterns(
#     path("admin/", admin.site.urls),
#     prefix_default_language=False
#     )
