"""book_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from mainapp.views import main, catalog, show_book_info, contacts, test


urlpatterns = [
    path('', main, name='main'),
    path('catalog/', include('mainapp.urls')),
    path('contacts/', contacts, name='contacts'),
    path('test/', test, name='test'),
    path('auth/', include('auth_app.urls', namespace='auth')),
    path('libr/', include('userlibrapp.urls', namespace='libr')),
    path('myadmin/', include('admin_app.urls', namespace='admin')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
