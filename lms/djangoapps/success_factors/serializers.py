from rest_framework import serializers
from success_factors.models import CompletionStatusEvent


class CompletionStatusEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletionStatusEvent
        fields = (
            'id',
            'enterprise_customer_user_id',
            'sf_user_id',
            'course_id',
            'course_completed',
            'completed_timestamp',
            'instructor_name',
            'grade',
        )


