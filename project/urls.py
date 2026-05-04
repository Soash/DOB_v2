from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from service.sitemaps import ServiceSitemap, ClinicalServiceSitemap, StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'services': ServiceSitemap,
    'clinical_services': ClinicalServiceSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('services/', include('service.urls')),
    path('bsds/', include('bsds.urls')),
    path("__reload__/", include("django_browser_reload.urls")), 
    path('tinymce/', include('tinymce.urls')),
    
    # SEO
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
