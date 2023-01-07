from django.db import models

# Create your models here.
class NewsDomainLink(models.Model):
    domain_id = models.IntegerField(null=False)
    domain_name = models.CharField(null=False, max_length=255)
    site_id = models.IntegerField(null=False)
    site_name = models.CharField(null=False, max_length=255)
    domain_url = models.TextField(null=False, max_length=1000)
    domain_slug = models.TextField(null=False, max_length=1000)
    is_active = models.BooleanField(default=True)

    # def __str__(self):
    #     return self.domain_name


class NewsSite(models.Model):
    site_name = models.CharField(null=False, max_length=255)
    site_name_bn = models.CharField(null=False, max_length=255)
    is_bengali = models.BooleanField()
    is_english = models.BooleanField()
    site_url = models.TextField(null=False, max_length=1000)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.site_name

