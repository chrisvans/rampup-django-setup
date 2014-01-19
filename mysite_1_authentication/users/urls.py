from django.conf.urls import patterns, url

from users import views

urlpatterns = patterns('',
    url(r'^$', views.login_view, name='login'),
    url(r'^register/', views.registration_view, name='register'),
)