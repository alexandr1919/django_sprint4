from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('pages/', include('pages.urls'), name='pages'),
    path('', include('authorization.urls', namespace='authorization')),
    path('', include('blog.urls', namespace='blog')),
]
