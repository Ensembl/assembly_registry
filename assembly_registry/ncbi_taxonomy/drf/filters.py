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

import coreapi
from rest_framework.filters import BaseFilterBackend
from ncbi_taxonomy.utils import NcbiTaxonomyUtils


taxonomy_id_field = coreapi.Field(name='taxonomy_id',
                                  location='query',
                                  required=False,
                                  type='integer',
                                  description='taxonomy_id to filter (eg: 9606)')

taxonomy_ids_field = coreapi.Field(name='taxonomy_ids',
                                   location='query',
                                   required=False,
                                   type='string',
                                   description='taxonomy_ids to filter (eg: 9606, 10090)')

taxonomy_branch_field = coreapi.Field(name='taxonomy_branch',
                                      location='query',
                                      required=False,
                                      type='string',
                                      description='taxonomy_branch to filter (eg: 10090)')

taxonomy_name_field = coreapi.Field(name='taxonomy_name',
                                    location='query',
                                    required=False,
                                    type='string',
                                    description='taxonomy_name to filter (eg: human, homo sapiens, man)')

taxonomy_name_class_field = coreapi.Field(name='name_class',
                                          location='query',
                                          required=False,
                                          type='string',
                                          description='name_class to filter (eg: scientific name,authority, synonym)')


class TaxonomyFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):

        # Filter to filter by taxonomy_id.
        taxonomy_ids = request.query_params.get('taxonomy_ids', None)
        if taxonomy_ids is not None:
            ids = [int(taxid.strip()) for taxid in taxonomy_ids.split(',')]
            queryset = queryset.filter(taxon_id__in=ids)

        taxonomy_name = request.query_params.get('taxonomy_name', None)
        if taxonomy_name is not None:
            queryset = queryset.filter(name__icontains=taxonomy_name)

        name_class = request.query_params.get('name_class', None)
        if name_class is not None:
            queryset = queryset.filter(name_class=name_class)

        taxonomy_branch = request.query_params.get('taxonomy_branch', None)
        if taxonomy_branch is not None:
            descendant_tax_ids = NcbiTaxonomyUtils.fetch_descendant_ids(taxonomy_branch)
            print(descendant_tax_ids)
            queryset = queryset.filter(taxon_id__in=descendant_tax_ids)

        return queryset

    def get_schema_fields(self, view):
        return [taxonomy_ids_field, taxonomy_name_field, taxonomy_branch_field, taxonomy_name_class_field]
