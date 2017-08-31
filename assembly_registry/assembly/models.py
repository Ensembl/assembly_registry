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
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver
from django.db.models.aggregates import Max
from django.core.exceptions import ObjectDoesNotExist, SuspiciousOperation


class Assembly(models.Model):

    assembly_id = models.AutoField(primary_key=True, auto_created=True)
    project_name = models.CharField(max_length=200)
    genus = models.CharField(max_length=10, null=True, blank=True)
    scientific_name = models.CharField(max_length=200)
    encoded_name = models.CharField(max_length=200, unique=True, editable=False)
    taxon_id = models.IntegerField(null=True, blank=True)
    centre = models.CharField(max_length=200)
    status = models.CharField(max_length=200, null=True, blank=True)
    data_release = models.CharField(max_length=200, null=True, blank=True)
    version = models.IntegerField(null=True, blank=True)
    created_by = models.ForeignKey('auth.User', related_name='user', on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = 'assembly'

    def derive_encoded_name(self):
        """
        encoded_name = first character from genus (f or m) +
                      first 3 characters from scientific name species +
                      first 3 characters from scientific name genus +
                      aseembly version (if the species already exist, increment it)
        eg:  female + Astatotilapia calliptera + 2 + fAstCal2
        """
        genus = self.genus
        scientific_name = self.scientific_name
        assembly_version = self.version

        genus_first_char = ''
        if genus is not None:
            genus_first_char = genus[:1]

        species_first3 = ''
        if scientific_name is not None:
            spe_genus = scientific_name.split()
            if len(spe_genus) == 2 and len(spe_genus[0]) >= 3 and len(spe_genus[1]) >= 3:
                species_first3 = spe_genus[0][:3].title() + spe_genus[1][:3].title()
            elif len(spe_genus) == 1 and len(spe_genus[0]) >= 3:
                species_first3 = spe_genus[0][:3].title()
            else:
                raise SuspiciousOperation("Please check the scientific name " + scientific_name +
                                          ". It seems to be not in the right format")

        gen_spe = genus_first_char + species_first3

        new_assembly_version = 1
        assembly_version_cur_max = None
        if assembly_version is None or assembly_version == 0:
            # check is there is another entry with the same scientific name
            assembly_version_cur_max_dict = Assembly.objects.\
                filter(encoded_name__startswith=gen_spe).\
                aggregate(Max('version'))

            if assembly_version_cur_max_dict['version__max'] is not None:
                assembly_version_cur_max = assembly_version_cur_max_dict['version__max'] + 1
                new_assembly_version = assembly_version_cur_max
            else:
                new_assembly_version = 1
        else:
            new_assembly_version = assembly_version

        encoded_name = genus_first_char + species_first3 + str(new_assembly_version)
        return (encoded_name, new_assembly_version)


@receiver(pre_save, sender=Assembly, dispatch_uid='assembly_registry.models.assembly_pre_save_handler')
def assembly_pre_save(sender, instance, **kwargs):
    """ This method is executed before an assembly object is created  """
    # update the encoded_name only if it is not none
    if instance.encoded_name is None or len(instance.encoded_name) == 0:
        (encoded_name, new_assembly_version) = instance.derive_encoded_name()

        assembly_check_if_exists = None
        try:
            assembly_check_if_exists = Assembly.objects.get(encoded_name=encoded_name)
        except ObjectDoesNotExist:
            pass

        if assembly_check_if_exists is None:
            instance.encoded_name = encoded_name
            instance.version = new_assembly_version
        else:
            raise SuspiciousOperation("Assembly with same encoded_name  " + assembly_check_if_exists.encoded_name +
                                      " already exists. Please check/update the version ")
