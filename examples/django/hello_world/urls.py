from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^$', 'hello_world.views.home', name='home'),
)
