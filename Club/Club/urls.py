from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import static,staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    path('Admin/',include('Custom_Admin.urls')),
    path('Member/',include('Member.urls')),
    path('Club/',include('Home.urls')),
    path('Club/',include('Inquiry.urls')),
    path('Club/',include('Amenities.urls')),
    path('Club/',include('Payments.urls')),
    path('Club/',include('Plans.urls')),
    path('Club/',include('Events.urls')),
    path('Club/',include('Feedback.urls')),
    path('Payments/',include('Payments.urls')),

    path('paypal/', include('paypal.standard.ipn.urls')),
]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)