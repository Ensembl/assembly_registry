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
from ncbi_taxonomy.models import NcbiTaxaName, NcbiTaxaNode


class NcbiTaxaNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = NcbiTaxaName
        fields = '__all__'


class NcbiTaxaNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NcbiTaxaNode
        fields = '__all__'
