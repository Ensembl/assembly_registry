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

from django.conf.urls import url
from assembly import views
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^$', views.AssemblyList.as_view(), name='assembly_list'),
    url(r'^encoded_name/(?P<encoded_name>[a-zA-Z0-9]+)/$', views.AssemblyDetail.as_view(), name='assembly_detail'),
    url(r'^datatable/list', TemplateView.as_view(template_name="assembly_datatable.html"), name="assembly_datatable"),
    url(r'^help/$', TemplateView.as_view(template_name="assembly_help.html"),
        {"hostname": "http://prem-ml:9000"}, name="assembly_help"),
    url(r'^listall', views.AssemblyListNopagination.as_view(), name="assembly_nopagination_datatable"),

]
