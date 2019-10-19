import unittest
from services.ctyimport import CtyImportLib

from model import model
from model.model import MySQLDatabase
from os import getenv
import os
import config
from common.common import BaseUseCase


class CtyImport(BaseUseCase):

    def execute(self, content, **kwargs):
        user_data=None
        if 'user_data' in kwargs:
            user_data=kwargs['user_data']

        content=content.split('\n')

        @CtyImportLib
        def test(country, **kwargs):
            user_data=None
            if 'user_data' in kwargs:
                user_data=kwargs['user_data']
            dxcc=model.LogDxcc.get_or_none(model.LogDxcc.id==country['prefix'])
            if dxcc==None:
                dxcc=model.LogDxcc()

            dxcc.continent=country['continent']
            dxcc.country=country['country']
            dxcc.cq_zone=country['cq']
            dxcc.itu_zone=country['itu']
            dxcc.time_offset=float(country['time_offset']) 
            dxcc.longitude=float(country['longitude'])
            dxcc.latitude=float(country['latitude'])
            dxcc.entity=0

            if dxcc.id==None:
                dxcc.id=country['prefix']
                dxcc.save(force_insert=True)
            else:
                dxcc.save()


            for item in country['prefixes']:
                prefix=item['prefix']
                exact_match=item['match']
                exists=True

                dxcc_pref=model.LogDxccPrefixes.get_or_none(model.LogDxccPrefixes.id==prefix)
                if dxcc_pref==None:
                    exists=False
                    dxcc_pref=model.LogDxccPrefixes()           

                dxcc_pref.dxcc_id=country['prefix']
                dxcc_pref.cq_zone=country['cq']
                dxcc_pref.itu_zone=country['itu']
                dxcc_pref.time_offset=float(country['time_offset']) 
                dxcc_pref.entity=0
                dxcc_pref.id=prefix
                dxcc_pref.exact_match=exact_match
                dxcc_pref.save(force_insert=not exists)

            self._execute('after_save_cty_rec', record=country, user_data=user_data)
            pass

        test(content, user_data=user_data)

