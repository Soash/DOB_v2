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
