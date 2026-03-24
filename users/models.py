from django.contrib.auth.models import AbstractUser
from django.db import models

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
    
    # Optional social/profile links
    photo = models.ImageField(upload_to='team_photos/', blank=True, null=True)
    facebook = models.URLField(max_length=200, blank=True, null=True)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    portfolio = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.username
