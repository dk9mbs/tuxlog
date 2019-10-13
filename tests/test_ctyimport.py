import unittest
from services.ctyimport import CtyImportLib

from model import model
from model.model import MySQLDatabase
from os import getenv
import os
import config



class TestCtyImport(unittest.TestCase):
    def test_import_ctydat(self):
        config.DatabaseConfig.open(model.database, config.DatabaseConfig.read_from_file(os.getenv("tuxlog_environment")))

        content="Sov Mil Order of Malta:   15:  28:  EU:   41.90:   -12.43:    -1.0:  1A:\n" \
        "    1A;\n" \
        "Spratly Islands:          26:  50:  AS:    9.88:  -114.23:    -8.0:  1S:\n" \
        "    9M0,BM9S,BN9S,BO9S,BP9S,BQ9S,BU9S,BV9S,BW9S,BX9S;\n" \
        "Monaco:                   14:  27:  EU:   43.73:    -7.40:    -1.0:  3A:\n" \
        "    3A;\n" \
        "Agalega & St. Brandon:    39:  53:  AF:  -10.45:   -56.67:    -4.0:  3B6:\n" \
        "    3B6,3B7;\n" \
        "Mauritius:                39:  53:  AF:  -20.35:   -57.50:    -4.0:  3B8:\n" \
        "    3B8;\n" \
        "Rodriguez Island:         39:  53:  AF:  -19.70:   -63.42:    -4.0:  3B9:\n" \
        "    3B9;\n"

        content=content.split('\n')

        with open('/tmp/cty.dat', 'r') as file:
            content=file.readlines()


        @CtyImportLib
        def test(country, **kwargs):
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


            print('%s => %s (%s) offset:%s' % (country['prefix'], country['country'], country['continent'], country['time_offset'])  )
            pass

        test(content)

        #self.assertEqual(test, 'xxx')

if __name__ == '__main__':
    unittest.main()