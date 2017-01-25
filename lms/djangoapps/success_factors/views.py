import requests
import time
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from success_factors.models import CompletionStatusEvent, OCNWebServicesConfig, OCNEnterpriseCustomerConfig
from success_factors.serializers import CompletionStatusEventSerializer

# Create your views here.


class SuccessFactorsList(APIView):
    def get(self, request, format=None):
        completion_statuses = CompletionStatusEvent.objects.all()
        serializer = CompletionStatusEventSerializer(completion_statuses, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CompletionStatusEventSerializer(data=request.data)
        if serializer.is_valid():
            ocn_web_services_config = OCNWebServicesConfig.objects.get(pk=1)
            ocn_enterprise_customer_config = OCNEnterpriseCustomerConfig.objects.get(pk=1)
            sf_url = ocn_enterprise_customer_config.sf_base_url + '/' + ocn_web_services_config.completion_status_api_path
            sf_payload = {
                'userID': serializer.data['sf_user_id'],
                'courseID': serializer.data['course_id'],
                'providerID': 'EDX',
                'courseCompleted': True,
                'completedTimestamp': int(time.time()),
                'instructorName': serializer.data['instructor_name'],
                'grade': serializer.data['grade']
            }

            response = requests.post(sf_url, data=sf_payload)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SuccessFactorsDetail(APIView):
    def get_object(self, pk):
        try:
            return CompletionStatusEvent.objects.get(pk=pk)
        except CompletionStatusEvent.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        completion_status = self.get_object(pk)
        serializer = CompletionStatusEventSerializer(completion_status)
        return Response(serializer.data)




