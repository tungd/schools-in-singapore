from django.db import models


class School(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField()
    address = models.TextField()
    postal_code = models.IntegerField()
    phone_number = models.CharField(max_length=255)
    fax_number = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    vision_statement = models.TextField()
    mission_statement = models.TextField()
    philosophy = models.TextField(null=True, blank=True)
    dgp_code = models.CharField(max_length=255)
    zone_code = models.CharField(max_length=255)
    cluster_code = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    session = models.CharField(max_length=255)
    main_level = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    offer = models.TextField()
