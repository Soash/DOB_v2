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
