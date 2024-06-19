
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from .import settings
from group.context_processors import remove_group
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [
    path("admin/", admin.site.urls),
    path("",include(('home.urls','index'),namespace='index')),
    path("account/",include(('account.urls','account'),namespace='account')),
    path('g/',include(('group.urls','group'),namespace='group')),
    path('g/',include(('post.urls','post'),namespace='post')),
    path('u/',include(('user.urls','user'),namespace='user')),
    path('chat/',include(('chat.urls','chat'),namespace="chat")),
    path('search/',include(('search.urls','search'),namespace="search")),
    path("remove_group/<slug:slug>",remove_group,name="remove_group")
 
  

    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()