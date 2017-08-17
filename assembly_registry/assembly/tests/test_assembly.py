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

from rest_framework.test import APITestCase
from assembly.models import Assembly
import json
from django.urls.base import reverse
from django.contrib.auth.models import User


class AssemblyTest(APITestCase):
    fixtures = ['assembly']
#     multi_db = True

    def test_loaddata(self):
        assembly = Assembly.objects.get(pk=1)
        self.assertEqual(1, assembly.assembly_id)
        self.assertEqual('VGP', assembly.project_name)
        all_ = Assembly.objects.all()
        self.assertEquals(len(all_), 5)

        testuser = User.objects.get(username='test1')
        self.assertEqual('test1', testuser.username)
        self.assertEqual('TestFirst', testuser.first_name)
        self.assertEqual('TestLast', testuser.last_name)

    def test_api_request(self):
        # Using the standard APIClient to create a GET request

        # Test the assembly list
        response = self.client.get('/assembly/')
        self.assertEqual(response.status_code, 200)
        json_response = (json.loads(response.content.decode('utf8')))
        self.assertEqual(json_response['count'], 5)
        expected_assembly = {'scientific_name': 'Astatotilapia calliptera', 'data_release': 'public',
                             'gender': 'female', 'centre': 'WTSI', 'status': 'genome sequenced',
                             'modified_date': '2017-08-03T13:01:53Z',
                             'created_date': '2017-08-03T13:01:53Z',
                             'taxon_id': 8152, 'gen_spe_num': 'fAstCal1',
                             'project_name': 'VGP', 'assembly_id': 1,
                             'assembly_version': 1, 'username': 'test2'}

        self.assertEqual(json_response['results'][0], expected_assembly)
        # Test filter by gen_spe_num
        response = self.client.get('/assembly/gen_spe_num/fAstCal1/')
        self.assertEqual(response.status_code, 200)
        json_response = (json.loads(response.content.decode('utf8')))
        self.assertEqual(json_response, expected_assembly)

        # POST
        url = reverse('assembly_list')
        data = {'scientific_name': 'Astatotilapia calliptera', 'data_release': 'public',
                'gender': 'female', 'centre': 'WTSI', 'status': 'genome sequenced',
                'project_name': 'VGP',
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)  # Unauthorized

        # Login
        test_user2 = User.objects.get(username="test2")
        self.assertIsNotNone(test_user2, "got test2 user")
        self.client.force_authenticate(user=test_user2)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)  # Created

        # PUT (UPDATE)
        url = "/assembly/gen_spe_num/fAstCal1/"
        data = {'scientific_name': 'Astatotilapia calliptera'
                }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 400)  # Bad request.Not allowed to update scientific_name

        data = {'gender': 'male'
                }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 400)  # Bad request.Not allowed to update gender

        data = {'assembly_version': '2'
                }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 400)  # Bad request. Not allowed to update gender assembly_version

        data = {'project_name': 'updated_project_name'
                }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)  # OK

        assembly = Assembly.objects.get(gen_spe_num="fAstCal1")
        self.assertEqual("updated_project_name", assembly.project_name, "Updated successfully")

        # DELETE
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, 204)  # No content

    def test_derive_gen_spe_num(self):

        assembly_fAstCal1 = Assembly.objects.get(gen_spe_num="fAstCal1")
        self.assertEqual("female", assembly_fAstCal1.gender, "Got the right gender")
        self.assertEqual("Astatotilapia calliptera", assembly_fAstCal1.scientific_name, "Got the right scientific_name")
        self.assertEqual(1, assembly_fAstCal1.assembly_version, "Got the right assembly version")

        assembly_fAstCal1 = Assembly.objects.get(gen_spe_num="fAstCal3")
        self.assertEqual("female", assembly_fAstCal1.gender, "Got the right gender")
        self.assertEqual("Astatotilapia calliptera", assembly_fAstCal1.scientific_name, "Got the right scientific_name")
        self.assertEqual(3, assembly_fAstCal1.assembly_version, "Got the right assembly version")

        assembly_fAstCal1 = Assembly.objects.get(gen_spe_num="mHomSap1")
        self.assertEqual("male", assembly_fAstCal1.gender, "Got the right gender")
        self.assertEqual("Homo sapiens", assembly_fAstCal1.scientific_name, "Got the right scientific_name")
        self.assertEqual(1, assembly_fAstCal1.assembly_version, "Got the right assembly version")
