from django.contrib.auth.models import AbstractUser
from django.db import models
from tinymce.models import HTMLField

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="e.g. IT, Research, HR")
    order = models.IntegerField(default=0, help_text="Used to sort departments in the UI")

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    role = models.CharField(max_length=100, blank=True, help_text="e.g. Senior Bioinformatician")
    bio = models.TextField(blank=True, null=True, help_text="Brief biography")
    order_in_department = models.IntegerField(default=0, help_text="Sorting order within the department")
    
    # Profile & Career Info
    degree = models.CharField(max_length=150, blank=True, null=True, help_text="BSc / MSc / PhD / Degree Title")
    university = models.CharField(max_length=255, blank=True, null=True, help_text="University Name")
    country = models.CharField(max_length=100, blank=True, null=True, help_text="Country Name")
    education = models.TextField(blank=True, null=True, help_text="Additional education notes (optional)")
    skills = models.CharField(max_length=500, blank=True, null=True, help_text="Comma-separated skills (e.g. Next-Generation Sequencing, Python, Molecular Docking, R)")
    career_progression_details = HTMLField(blank=True, null=True, help_text="Rich text editor for detailed career progression, achievements, or research summary")
    
    # Media and Social links
    photo = models.ImageField(upload_to='team_photos/', blank=True, null=True)
    facebook = models.URLField(max_length=255, blank=True, null=True)
    linkedin = models.URLField(max_length=255, blank=True, null=True)
    portfolio = models.URLField(max_length=255, blank=True, null=True)
    github = models.URLField(max_length=255, blank=True, null=True)
    researchgate = models.URLField(max_length=255, blank=True, null=True)
    google_scholar = models.URLField(max_length=255, blank=True, null=True)
    twitter = models.URLField(max_length=255, blank=True, null=True)

    @property
    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        from django.templatetags.static import static
        return static('images/profile.jpg')

    @property
    def get_education_list(self):
        records = list(self.educations.all())
        if records:
            return records
        if self.degree or self.university or self.country:
            return [{
                'degree': self.degree or 'Degree',
                'university': self.university or '',
                'country': self.country or '',
            }]
        if self.education:
            return [{
                'degree': self.education,
                'university': '',
                'country': '',
            }]
        return []

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.username


class Education(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=150, help_text="BSc / MSc / PhD / Degree Title")
    university = models.CharField(max_length=255, help_text="University Name")
    country = models.CharField(max_length=100, blank=True, help_text="Country Name")
    order = models.PositiveIntegerField(default=0, help_text="Sort order")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Education"
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.user.username} - {self.degree} ({self.university})"


class CareerProgression(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='career_milestones')
    title = models.CharField(max_length=200, help_text="Position / Role / Milestone title (e.g. Senior Bioinformatician)")
    organization = models.CharField(max_length=200, blank=True, help_text="Organization / Institution / Department (e.g. Dawn of Bioinformatics)")
    start_date = models.DateField(null=True, blank=True, help_text="Start date (e.g. 01 Jan 2025)")
    end_date = models.DateField(null=True, blank=True, help_text="End date (e.g. 30 June 2025, leave blank if currently in this role)")
    period = models.CharField(max_length=100, blank=True, help_text="Custom period fallback (e.g. from 01 Jan 2025 to 30 June 2025)")
    description = models.TextField(blank=True, help_text="Responsibilities, promotions, research focus, or achievements")
    is_current = models.BooleanField(default=False, help_text="Check if this is their current position")
    order = models.PositiveIntegerField(default=0, help_text="Sort order (lowest number appears first)")

    class Meta:
        ordering = ['order', '-id']
        verbose_name = "Career Milestone"
        verbose_name_plural = "Career Milestones"

    @property
    def formatted_start_date(self):
        if self.start_date:
            return self.start_date.strftime('%d %B %Y')
        return ""

    @property
    def formatted_end_date(self):
        if self.end_date:
            return self.end_date.strftime('%d %B %Y')
        return ""

    @property
    def duration_display(self):
        if not self.start_date:
            return ""
        from datetime import date
        end = self.end_date if (self.end_date and not self.is_current) else date.today()
        months = (end.year - self.start_date.year) * 12 + (end.month - self.start_date.month)
        if end.day >= self.start_date.day:
            months += 1
        months = max(1, months)
        years = months // 12
        rem_months = months % 12
        parts = []
        if years > 0:
            y_str = f"{years:02d}"
            parts.append(f"{y_str} year" if years == 1 else f"{y_str} years")
        if rem_months > 0:
            m_str = f"{rem_months:02d}"
            parts.append(f"{m_str} month" if rem_months == 1 else f"{m_str} months")
        if not parts:
            m_str = f"{months:02d}"
            parts.append(f"{m_str} month" if months == 1 else f"{m_str} months")
        return " ".join(parts)

    @property
    def date_display(self):
        if self.start_date and self.end_date:
            return f"from {self.formatted_start_date} to {self.formatted_end_date}"
        elif self.start_date and self.is_current:
            return f"from {self.formatted_start_date} to Present"
        elif self.start_date:
            return f"from {self.formatted_start_date}"
        elif self.period:
            return self.period
        return ""

    def __str__(self):
        d = self.date_display or "Undated"
        return f"{self.user.username} - {self.title} ({d})"
