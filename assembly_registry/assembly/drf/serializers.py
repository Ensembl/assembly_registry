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

from rest_framework import serializers
from assembly.models import Assembly
from assembly_registry.utils.drf_mixin import SerializerMixin

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    assemblys = serializers.PrimaryKeyRelatedField(many=True, queryset=Assembly.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'assemblys')


class AssemblySerializer(SerializerMixin, serializers.ModelSerializer):

    MANY2ONE_SERIALIZER = {}
    username = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Assembly
        # fields = '__all__'
        fields = ('assembly_id', 'project_name', 'encoded_name', 'taxon_id', 'centre', 'status',
                  'data_release', 'version', 'genus', 'scientific_name', 'created_date',
                  'modified_date', 'username')
