from django.db import models
from config_models.models import ConfigurationModel

# Create your models here.


class CompletionStatusEvent(models.Model):
    """
    This represents the payload we sent to Success Factors at a given point in time for an enterprise customer user.
    """
    created = models.DateTimeField(auto_now_add=True)
    enterprise_customer_user_id = models.IntegerField()
    sf_user_id = models.CharField(max_length=260)
    course_id = models.CharField(max_length=260)
    course_completed = models.BooleanField(default=True)
    completed_timestamp = models.DateTimeField(auto_now_add=True)
    instructor_name = models.CharField(max_length=260, blank=True)
    grade = models.CharField(max_length=100)

    class Meta:
        ordering = ('created',)


class OCNEnterpriseCustomerConfig(ConfigurationModel):
    """
    This represents the Enterprise specific configuration we need for integrating with SuccessFactors.
    """
    enterprise_customer_uuid = models.UUIDField(unique=True)
    sf_base_url = models.CharField(max_length=260)
    provider_slug = models.SlugField(max_length=30, db_index=True)
    key = models.TextField(blank=True, verbose_name="Client ID")
    secret = models.TextField(blank=True, verbose_name="Client Secret")


class OCNWebServicesConfig(ConfigurationModel):
    """
    This represents global configuration for integrating with SuccessFactors.
    """
    completion_status_api_path = models.CharField(max_length=260)
    course_api_path = models.CharField(max_length=260)
    oauth_api_path = models.CharField(max_length=260)
    provider_id = models.CharField(max_length=100, default='EDX')
