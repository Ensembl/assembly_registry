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


from rest_framework.filters import BaseFilterBackend
from rest_framework.compat import coreapi

# Fields
project_name_field = coreapi.Field(
            name='project_name',
            location='query',
            required=False,
            type='string',
            description='project_name to filter(eg: VGP)')

encoded_name = coreapi.Field(
            name='encoded_name',
            location='query',
            required=False,
            type='string',
            description='encoded_name to filter(eg: fAstCal2)')

genus_field = coreapi.Field(
            name='genus',
            location='query',
            required=False,
            type='string',
            description='genus to filter')

scientific_name_field = coreapi.Field(
            name='scientific_name',
            location='query',
            required=False,
            type='string',
            description='scientific_name to filter(eg: Homo sapiens)')

version_field = coreapi.Field(
            name='version',
            location='query',
            required=False,
            type='string',
            description='version to filter(eg: 1, 2)')

taxonomy_ids_field = coreapi.Field(name='taxonomy_ids',
                                   location='query',
                                   required=False,
                                   type='string',
                                   description='taxonomy_ids to filter (eg: 8152, 9606)')

centre_field = coreapi.Field(
            name='centre',
            location='query',
            required=False,
            type='string',
            description='centre to filter(eg: WTSI)')

status_field = coreapi.Field(
            name='status',
            location='query',
            required=False,
            type='string',
            description='status to filter(eg: submitted)')

data_release_field = coreapi.Field(
            name='data_release',
            location='query',
            required=False,
            type='string',
            description='data_release to filter(eg: private )')


class AssemblyFilterBackend(BaseFilterBackend):
    """
    Filter to filter by assembly fields
    """
    def filter_queryset(self, request, queryset, view):
        project_name = request.query_params.get('project_name', None)
        if project_name is not None:
            queryset = queryset.filter(project_name__icontains=project_name)

        encoded_name = request.query_params.get('encoded_name', None)
        if encoded_name is not None:
            queryset = queryset.filter(encoded_name__icontains=encoded_name)

        taxonomy_ids = request.query_params.get('taxonomy_ids', None)
        if taxonomy_ids is not None:
            ids = [int(taxid.strip()) for taxid in taxonomy_ids.split(',')]
            queryset = queryset.filter(taxon_id__in=ids)

        centre = request.query_params.get('centre', None)
        if centre is not None:
            queryset = queryset.filter(centre__icontains=centre)

        genus = request.query_params.get('genus', None)
        if genus is not None:
            queryset = queryset.filter(genus=genus)

        version = request.query_params.get('version', None)
        if version is not None:
            queryset = queryset.filter(version=version)

        scientific_name = request.query_params.get('scientific_name', None)
        if scientific_name is not None:
            queryset = queryset.filter(scientific_name__icontains=scientific_name)

        status = request.query_params.get('status', None)
        if status is not None:
            queryset = queryset.filter(status__icontains=centre)

        data_release = request.query_params.get('data_release', None)
        if data_release is not None:
            queryset = queryset.filter(data_release__icontains=data_release)

        return queryset

    def get_schema_fields(self, view):
        return [project_name_field, encoded_name, genus_field, scientific_name_field, version_field,
                taxonomy_ids_field, centre_field, status_field, data_release_field]
