from django.conf.urls import url

from blog.views import home, post_detail, login_page, new_post, edit_post, del_post, del_com, view_drafts, comm_edit

urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'^(?P<postno>[0-9]+)/$', post_detail, name = "post"),
    url(r'^(?P<postno>[0-9]+)/editcom/(?P<comno>[0-9]+)', comm_edit),
    url(r'^login/', login_page, name = "login" ),
    url(r'^newpost/', new_post, name = "newpost" ),
    url(r'^editpost/(?P<pk>[0-9]+)', edit_post, name = "editpost" ),
    url(r'^deletepost/(?P<pk>[0-9]+)', del_post),
    url(r'^(?P<postno>[0-9]+)/delcom/(?P<comno>[0-9]+)',del_com),
    url(r'^drafts/', view_drafts)

]
