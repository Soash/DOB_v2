from django.db import models
from django.utils.text import slugify

class BSDSItem(models.Model):
    title = models.CharField(max_length=200, help_text="e.g., Bioinformatics Research Wings")
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    
    # Media and Links
    thumbnail = models.ImageField(
        upload_to='bsds/thumbnails/', 
        blank=True, 
        null=True, 
        help_text="Upload an image for this BSDS item"
    )
    details_url = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="Link for the 'Details' button. Can be a full URL or relative path."
    )
    
    # Ordering and Status
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Order in which this item appears on the page")

    class Meta:
        verbose_name = "BSDS Item"
        verbose_name_plural = "BSDS Items"
        ordering = ['order', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



