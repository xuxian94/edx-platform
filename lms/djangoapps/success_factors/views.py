from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from success_factors.models import CompletionStatusEvent
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

    def put(self, request, pk, format=None):
        completion_status = self.get_object(pk)
        serializer = CompletionStatusEventSerializer(completion_status, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        completion_status = self.get_object(pk)
        completion_status.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



