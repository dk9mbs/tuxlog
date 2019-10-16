import unittest
from services.ctyimport import CtyImportLib

from model import model
from model.model import MySQLDatabase
from os import getenv
import os
import config
from usecases.ctyimport import CtyImport


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

        #content=content.split('\n')

        #with open('/tmp/cty.dat', 'r') as file:
        #    content=file.readlines()

        uc=CtyImport()
        uc.execute(content)


if __name__ == '__main__':
    unittest.main()