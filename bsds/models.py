from django.db import models


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


class CampusSeminar(models.Model):
    abbreviation = models.CharField(max_length=20, help_text="Short code, e.g. DU, JU, CU")
    university_name = models.CharField(max_length=255, help_text="Full university name")
    event_description = models.CharField(max_length=255, help_text="e.g. October 2023 • Genomic Sequencing Workshop")
    image = models.ImageField(upload_to='campus_seminars/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Campus Seminar"
        verbose_name_plural = "Campus Seminars"

    def __str__(self):
        return f"{self.abbreviation} – {self.university_name}"

    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return 'https://lh3.googleusercontent.com/aida-public/AB6AXuCkXDLCMLWvnv9wlFT_oS7Z3hTbKOS603ECvZpfXcS5927jXqjDFg4298UCBSp2e-qyOPxFIMu4MR4SaDvh3UcVqAOoOZM3vII5vdHMy6wbB-as7EaI0K5nqAaJReUN_zSnl8FPdprf1bBdN2XLFJygnJla1yjVONHPCaDV4DNXcXumJJHiXo1g43WTcAfSFIJvCHzlmDZLnWoPsEib7q_3bK-O-7ho9O_nZIyKFasYhlE5rmQ0mHPpj0DdHmcB72tv10wLkLTPWg'


class SeminarProgramConfig(models.Model):
    """
    Singleton configuration model for the On-Campus Seminar page links.
    Only one instance should ever be created via the admin.
    """
    bio_seminar_url = models.URLField(
        blank=True,
        help_text="'Request This Program' link for the On Campus Free Bioinformatics Seminar card."
    )
    clinical_seminar_url = models.URLField(
        blank=True,
        help_text="'Request This Program' link for the On Campus Free Clinical Bioinformatics Seminar card."
    )
    training_program_url = models.URLField(
        blank=True,
        help_text="'Request This Program' link for the On-Campus Bioinformatics Based Training Program card."
    )
    quiz_url = models.URLField(
        blank=True,
        help_text="URL for the 'Take the Seminar Quiz' button shown between the program cards and intro section."
    )

    class Meta:
        verbose_name = "Seminar Program Config"
        verbose_name_plural = "Seminar Program Config"

    def __str__(self):
        return "On-Campus Seminar Page Configuration"


# ── Campus Coordinators ────────────────────────────────────────────────────────

class CampusCoordinator(models.Model):
    year = models.PositiveIntegerField(help_text="Award year, e.g. 2026")
    name = models.CharField(max_length=255)
    role_label = models.CharField(max_length=255, help_text="e.g. Best Bioinformatics Campus Coordinator 2025")
    description = models.TextField()
    image = models.ImageField(upload_to='campus_coordinators/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-year', 'order']
        verbose_name = "Campus Coordinator Honor"
        verbose_name_plural = "Campus Coordinator Honors"

    def __str__(self):
        return f"{self.year} – {self.name}"

    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return 'https://lh3.googleusercontent.com/aida-public/AB6AXuDhEVtwEJ4ejJwycLciWT5GaeS4V1Py4E6pQhDfxDhCkBNyinjgJDLzeW0b9YISMX2wfKfoDSB2ehkjbftGdCaY2OMSORHxfPd1CveByWj9nHWpyjRifpEqkI1JMc1Saqehpcba7d6QuAVyOh2JPXGfa46sJzBbquC075DIh48uRF-FYJGTPtBkLsPlK9wFYUv-zifgjzX-N4oxbd74x7gk-oLt7BU558YriNl21ESsHUlTUtIjnLkuqI3z1YRRnvBuV-jQUXuerA'


# ── Collaboration ──────────────────────────────────────────────────────────────

class Collaboration(models.Model):
    COLLAB_TYPE = [
        ('university', 'University'),
        ('club', 'Club / Student Org'),
    ]
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=100, default='school', help_text="Material Symbol icon name, e.g. 'school', 'biotech'")
    collab_type = models.CharField(max_length=20, choices=COLLAB_TYPE, default='university')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['collab_type', 'order', 'name']
        verbose_name = "Collaborator"
        verbose_name_plural = "Collaborators"

    def __str__(self):
        return f"[{self.get_collab_type_display()}] {self.name}"


# ── Competition ────────────────────────────────────────────────────────────────

class Competition(models.Model):
    PLACEMENT_CHOICES = [
        ('', 'Active Contest'),
        ('1st', '1st Place'),
        ('2nd', '2nd Place'),
        ('3rd', '3rd Place'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='competitions/', blank=True, null=True)
    apply_url = models.URLField(blank=True, help_text="Application / participation link")
    is_active = models.BooleanField(default=True, help_text="Active contest or past winner?")
    placement = models.CharField(max_length=10, choices=PLACEMENT_CHOICES, blank=True, default='', help_text="For past winners only")
    year = models.PositiveIntegerField(blank=True, null=True, help_text="Year, for past winners")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-is_active', 'order']
        verbose_name = "Competition"
        verbose_name_plural = "Competitions"

    def __str__(self):
        return self.title

    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return 'https://lh3.googleusercontent.com/aida-public/AB6AXuDn7OFTTUfT6_60bmcreGGZ9fMsG_pXuLW-sy710V_OFzgaPbvyUM5xIPzQWKwrzJAJbtWQaGm6WqEN9ILwPB-HD-mI0g7gbuaurwnH3CLFWgxtj5XPsUtU9rj0FGjAet9Y-ruEchIpzRE7uW2ksdiLxJdrm03O5Gc-r7yihJ3V-WlaqKZWy9iHGuAURMYEUqABzVN4l0LGT_0eJhcwb4KH7ogsELY-wfUJ-nKHKNvN_uDi5ZgbEBz7MlgZxbecA9Bg-aJ5L0lqjQ'


# ── Research Talk ──────────────────────────────────────────────────────────────

class ResearchTalk(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='research_talks/', blank=True, null=True)
    youtube_url = models.URLField(blank=True, help_text="YouTube or external video link")
    duration = models.CharField(max_length=20, blank=True, help_text="e.g. 45:12")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Research Talk"
        verbose_name_plural = "Research Talks"

    def __str__(self):
        return self.title

    @property
    def get_thumbnail_url(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return self.thumbnail.url
        return 'https://lh3.googleusercontent.com/aida-public/AB6AXuBu8ZCLh1POINOp6-iTOySmhEyazn1p8VHMcYepfhdEViievM_OWYUElQ1nBOJYUde-4fI3C5pc9Rb_APk6zvDKfISmdevavJygyMrIyI633royn7F7yCFcgGGIS31ynO3BxY7K8PIxaHXA4ki9mjPPaWa6d1aqfVpGCE5e043rK2Uk9RTMlGkCmUrhrI4RsuErT875rQMagl810rwuZY8QR_jhZV-J5q4tJzmayhOfzPmmn1D-AkBOZOsmhwn8Jw0ipWxYOFBi2Q'

