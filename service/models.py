from django.db import models
from django.utils.text import slugify

class ServiceCategory(models.Model):
    name = models.CharField(max_length=200, help_text="e.g., Computer-Aided Drug Design Services")
    slug = models.SlugField(unique=True, blank=True)
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
    description = models.TextField()
    
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
    order = models.PositiveIntegerField(default=0, help_text="Order in which the service appears in its category")

    class Meta:
        ordering = ['category', 'order', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    
    