from django.conf.urls import url

from blog.views import home, post_detail

urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'^(?P<postno>[0-9]+)', post_detail, name = "post"),
    
]
