from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import ReviewCreateView, HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('review/', ReviewCreateView.as_view(), name='review'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
