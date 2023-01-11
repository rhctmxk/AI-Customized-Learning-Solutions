"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('allauth.urls')),

    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('', include('main.urls', namespace='main')),
    path('note/', include('note.urls', namespace='note')),
    path('extest/', include('extest.urls', namespace='extest')),
    path('recommend/', include('recommend.urls', namespace='reco')),
    path('mypage/', include('mypage.urls', namespace='mypage')),
    path('search/', include('search.urls', namespace='search')),
    path('emotionDetect/', include('emotionDetect.urls', namespace='emotion')),
    path('group/', include('group.urls', namespace='group')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
