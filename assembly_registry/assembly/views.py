'''
Copyright [1999-2015] Wellcome Trust Sanger Institute and the EMBL-European Bioinformatics Institute
Copyright [2016-2017] EMBL-European Bioinformatics Institute

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from __future__ import unicode_literals
from assembly.models import Assembly
from assembly.drf.serializers import AssemblySerializer, UserSerializer
from rest_framework import generics, status, mixins, exceptions
from assembly.drf.filters import AssemblyFilterBackend
from assembly_registry.utils.decorators import setup_eager_loading
from rest_framework.pagination import PageNumberPagination

from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.response import Response
from django.http.response import Http404
from rest_framework.permissions import IsAuthenticated


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AssemblyList(generics.ListCreateAPIView):
    """
    get:
    Return a list of all the existing assemblys (pagination enabled).

    post:
    Create a new assembly instance.
    """
    queryset = Assembly.objects.order_by('pk')
    serializer_class = AssemblySerializer
    filter_backends = (AssemblyFilterBackend,)

    """
    post:
    Please enter the data as json formatted string
    """
    def post(self, request, format=None):  # @ReservedAssignment
        serializer = AssemblySerializer(data=request.data)
        permission_classes = (IsAuthenticated,)  # @UnusedVariable

        # custom validation
#         if "genus" in request.data.keys() and request.data["genus"] is not None and len(request.data["genus"]) > 0:
#             gender_ = request.data["genus"]
#             if gender_ not in ["male", "female"]:
#                 raise exceptions.ValidationError(detail="Not a valid gender value." +
#                                                  " Gender should be either male or female")

        if serializer.is_valid():
            serializer.save(created_by=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotPaginatedSetPagination(PageNumberPagination):
    page_size = None


class AssemblyDetail(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    """
    get:
    Return the assembly instance.

    put:
    Update the assembly instance.

    delete:
    Delete the assembly instance.
    """

    queryset = Assembly.objects.all()
    serializer_class = AssemblySerializer
    filter_backends = (AssemblyFilterBackend,)
    queryset = Assembly.objects.all()
    serializer_class = AssemblySerializer
    lookup_field = 'encoded_name'

    def get_object(self, encoded_name):
        try:
            return Assembly.objects.get(encoded_name=encoded_name)
        except Assembly.DoesNotExist:
            raise Http404

    def get(self, request, encoded_name, format=None):  # @ReservedAssignment
        assembly = self.get_object(encoded_name)
        serializer = AssemblySerializer(assembly)
        return Response(serializer.data)

    def put(self, request, encoded_name, format=None):  # @ReservedAssignment
        assembly = self.get_object(encoded_name)

        assembly_data_fields = list(request.data.keys())

        non_editable_fields = ['encoded_name', 'genus', 'scientific_name', 'assembly_version']
        if 'encoded_name' in assembly_data_fields or 'genus' in assembly_data_fields \
                or 'scientific_name' in assembly_data_fields or 'version' in assembly_data_fields:
            raise exceptions.ValidationError(detail="Sorry. Operation not permitted." +
                                             " You are trying to edit one of the  non-editable fields " +
                                             str(non_editable_fields))

        serializer = AssemblySerializer(assembly, data=request.data, partial=True)
        permission_classes = (IsAuthenticated,)  # @UnusedVariable

        is_authorized = self.has_object_permission(self.request, self, assembly)

        if serializer.is_valid() and is_authorized:
            serializer.save(created_by=self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            if not is_authorized:
                raise exceptions.PermissionDenied(detail="Sorry " + self.request.user.username +
                                                  ". You don't have permission to do that operation " +
                                                  "as you are not the owner of the record")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, encoded_name, format=None):  # @ReservedAssignment
        assembly = self.get_object(encoded_name)
        permission_classes = (IsAuthenticated, )  # @UnusedVariable

        is_authorized = self.has_object_permission(self.request, self, assembly)

        if is_authorized:
            assembly.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise exceptions.PermissionDenied(detail="Sorry. You don't have permission to do that operation")

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.created_by == request.user


class AssemblyListNopagination(generics.ListAPIView):
    """
    get:
    Return a list of all the existing assemblys (pagination disabled).
    """
    pagination_class = NotPaginatedSetPagination
    queryset = Assembly.objects.order_by('pk')
    serializer_class = AssemblySerializer
    filter_backends = (AssemblyFilterBackend,)

    @setup_eager_loading(AssemblySerializer)
    def get_queryset(self):
        queryset = Assembly.objects.order_by('pk')
        return queryset
