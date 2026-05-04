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

class Carrier(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    employment_type = models.CharField(max_length=100, help_text="e.g. Full-time, Part-time")
    location = models.CharField(max_length=100, help_text="e.g. Dhaka, Chittagong")
    vacancy = models.PositiveIntegerField(default=1)
    posted_date = models.DateField()
    deadline = models.DateField()
    short_description = models.TextField(help_text="Shown in the list view")
    job_overview = HTMLField(blank=True, null=True)
    required_profile = HTMLField(blank=True, null=True)
    role_description = HTMLField(blank=True, null=True)
    salary_info = HTMLField(blank=True, null=True)
    apply_url = models.URLField(blank=True, null=True, help_text="Link to external application form (e.g. Google Form). If empty, uses default mailto link.")
    
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-posted_date']
        verbose_name = "Career"
        verbose_name_plural = "Careers"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class BSDSEvent(models.Model):
    title = models.CharField(max_length=255)
    date_text = models.CharField(max_length=255, help_text="e.g. Oct 24 - 26, 2024")
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    
    class Meta:
        ordering = ['-id']
        
    def __str__(self):
        return self.title
        
    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return 'https://lh3.googleusercontent.com/aida-public/AB6AXuDxxSOkQEH_7av8ckby4tPkHp49HtySyomOTZCFYMJZ_NDhtX-bK_LqL3roDRv_VQKImgd8hnaNqFD84KTX0v2nvSLhE4JnBBUwXDKIQAecRRNPrUitbdJojQA37qnueHUFqyyyBp33yBLsYBYwCUCrnTSKMf4f3IOdpURebMhHUWVOYnYjKKVpCuTy8TpIOImtx73wEFTHg-bIAwHyLFRgNs_sxjz_fz1Y1qrT-_v7wpvugrQkRxhDBoqi-DVC_w5RS-DrNPvh7w'

