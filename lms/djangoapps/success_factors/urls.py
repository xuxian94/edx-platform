from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from success_factors import views

urlpatterns = [
    url(r'sf_completion_statuses/$', views.SuccessFactorsList.as_view()),
    url(r'sf_completion_statuses/(?P<pk>[0-9]+)/$', views.SuccessFactorsDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
