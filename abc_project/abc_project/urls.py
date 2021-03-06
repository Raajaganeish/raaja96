"""abc_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url
from abc_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.home,name='home'),
    url(r'^register/',views.index,name='index'),
    url(r'^login/',views.login,name='login'),
    url(r'^logout/',views.logout_view,name='logout'),
    url(r'^check',views.type_view,name='type_view'),
    url(r'^ajax_check',views.ajax_check,name='ajax_check'),
    url(r'^otp',views.otp,name='otp'),
    url(r'^display_data',views.display_data,name='display_data'),

]
