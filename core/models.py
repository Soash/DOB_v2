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

from tinymce.models import HTMLField
from django.conf import settings

class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Blog Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    content = HTMLField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    view_count = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ResearchPaper(models.Model):
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    publication_date = models.DateField()
    journal = models.CharField(max_length=255)
    abstract = models.TextField()
    link = models.URLField()
    image = models.ImageField(upload_to='research_papers/', blank=True, null=True)

    class Meta:
        ordering = ['-publication_date']

    def __str__(self):
        return self.title

class Feedback(models.Model):
    name = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    comment = models.TextField()
    star_count = models.PositiveIntegerField(default=5)
    image = models.ImageField(upload_to='feedback/', blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.name} - {self.occupation}"

    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        from django.templatetags.static import static
        return static('images/profile.jpg')

    @property
    def get_star_range(self):
        return range(self.star_count)
