from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'bookstr'

urlpatterns = [
    #/bookstr/
    url(r'^$',views.prelogin,name = 'prelogin'),
    url(r'^logins/$',views.logins,name = 'logins'),

    url(r'^logouts/$',views.logouts,name = 'logouts'),
    url(r'^ownersignin/$',views.ownsignin,name = 'ownersignin'),

    url(r'^reorder/$',views.reorder,name = 'reorder'),

    url(r'^signup/$',views.signup,name = 'signup'),
    url(r'^home/$',views.home,name = 'home'),
    url(r'^checkout/$',views.checkout,name = 'checkout'),
    url(r'^cardadder/$',views.cardadder,name = 'cardadder'),
    url(r'^search/$',views.search,name = 'search'),

    url(r'^checkedout/(?P<card_num>[0-9]+)/$',views.checkedout,name = 'checkedout'),


    url(r'^signup/custsignup/$',views.custsignup,name = 'custsignup'),



    #/bookstr/book/112
    url(r'^book/(?P<book_id>[0-9]+)/$', views.book, name = 'book_details'),
    url(r'^cart/$', views.cart, name = 'cart'),
    url(r'^cartadded/(?P<book_id>[0-9]+)/$', views.cartadded, name = 'cartadded'),
    url(r'^cartaddedbook/(?P<book_id>[0-9]+)/$', views.cartaddedbook, name = 'cartaddedbook'),


]
