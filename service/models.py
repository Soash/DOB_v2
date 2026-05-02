from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class ServiceCategory(models.Model):
    name = models.CharField(max_length=200, help_text="e.g., Computer-Aided Drug Design Services")
    short_name = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., CADD (used for tabs and tight spaces)")
    slug = models.SlugField(unique=True, blank=True)
    icon = models.ImageField(
        upload_to='service/category_icons/',
        blank=True,
        null=True,
        help_text="Upload a small icon for this category (displayed in tab buttons)"
    )
    order = models.PositiveIntegerField(default=0, help_text="Order in which the category appears")

    class Meta:
        verbose_name_plural = "Service Categories"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, related_name='services', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, help_text="e.g., Advanced Molecular Docking")
    slug = models.SlugField(unique=True, blank=True)
    
    # Existing description
    description = models.TextField()
    
    # New detailed description fields
    introduction_description = models.TextField(blank=True, null=True, help_text="Introduction content for the service page")
    features_description = models.TextField(blank=True, null=True, help_text="Details about the service features")
    demo_description = models.TextField(blank=True, null=True, help_text="Information regarding service demos or examples")
    
    # Image and Link fields
    thumbnail = models.ImageField(
        upload_to='service/thumbnails/', 
        blank=True, 
        null=True, 
        help_text="Upload an image for the service card"
    )
    learn_more_url = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="Link for the 'Learn more' button. Can be a full URL (https://...) or a relative path (/contact/)."
    )
    
    # Status and Ordering
    is_active = models.BooleanField(default=True)
    is_top = models.BooleanField(default=False, help_text="Check to display this service on the homepage's top section")
    order = models.PositiveIntegerField(default=0, help_text="Order in which the service appears in its category")

    class Meta:
        ordering = ['category', 'order', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('service:service_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


# --- NEW: Multiple Image System ---
class ServiceImage(models.Model):
    service = models.ForeignKey(Service, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='service/gallery/')
    caption = models.CharField(max_length=255, blank=True, help_text="Optional caption for the image")
    order = models.PositiveIntegerField(default=0, help_text="Order in which the image appears in the gallery")

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"Image for {self.service.title}"


# --- NEW: FAQ System ---
class ServiceFAQ(models.Model):
    service = models.ForeignKey(Service, related_name='faqs', on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0, help_text="Order in which the FAQ appears")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Service FAQ"
        verbose_name_plural = "Service FAQs"

    def __str__(self):
        return f"FAQ: {self.question} - {self.service.title}"

# --- NEW: Clinical Services ---

class ClinicalService(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(help_text="Short description for the home page card")
    
    # Icon and Styling
    icon_svg = models.TextField(blank=True, null=True, help_text="Paste SVG code here for the icon. Make sure to use 'currentColor' for stroke/fill.")
    icon_color = models.CharField(max_length=50, default='blue', help_text="Tailwind color name (e.g. blue, purple, cyan, teal, rose, amber)")
    
    # Detail page content
    introduction_description = models.TextField(blank=True, null=True)
    features_description = models.TextField(blank=True, null=True)
    demo_description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='clinical_service/thumbnails/', blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Clinical Service"
        verbose_name_plural = "Clinical Services"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('service:clinical_service_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class ClinicalServiceImage(models.Model):
    service = models.ForeignKey(ClinicalService, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='clinical_service/gallery/')
    caption = models.CharField(max_length=255, blank=True, help_text="Optional caption for the image")
    order = models.PositiveIntegerField(default=0, help_text="Order in which the image appears in the gallery")

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"Image for {self.service.title}"


class ClinicalServiceFAQ(models.Model):
    service = models.ForeignKey(ClinicalService, related_name='faqs', on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0, help_text="Order in which the FAQ appears")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Clinical Service FAQ"
        verbose_name_plural = "Clinical Service FAQs"

    def __str__(self):
        return f"FAQ: {self.question} - {self.service.title}"