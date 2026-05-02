from django.contrib.sitemaps import Sitemap
from .models import Service, ClinicalService
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['core:home', 'service:service_list', 'service:clinical_service_list', 'core:about', 'core:team', 'core:blog', 'core:research_papers']

    def location(self, item):
        return reverse(item)

class ServiceSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Service.objects.filter(is_active=True)

class ClinicalServiceSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ClinicalService.objects.filter(is_active=True)
