from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('signup/', views.signup_view, name = "signup"),
    path('login/', views.login_view, name = "login"),
    path('logout/', views.logout_view, name = "logout"),
    path('profile/<str:username>/', views.profile_view, name='profile'),
]

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

