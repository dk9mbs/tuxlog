import unittest
#from services.ctyimport import CtyImportLib
from usecases.ctyimport import CtyImportLib

from model import model
from model.model import MySQLDatabase
from os import getenv
import os
import config
from usecases.ctyimport import CtyImport
from jobs.ctyimportjob import CtyImportJob 


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
        "    3B9;\n" \
        "Fed. Rep. of Germany:     14:  28:  EU:   51.00:   -10.00:    -1.0:  DL:\n" \
        "    DA,DB,DC,DD,DE,DF,DG,DH,DI,DJ,DK,DL,DM,DN,DO,DP,DQ,DR,Y2,Y3,Y4,Y5,Y6,Y7,\n" \
        "    Y8,Y9;\n" \
        "Denmark:                  14:  18:  EU:   56.00:   -10.00:    -1.0:  OZ:\n" \
        "    5P,5Q,OU,OV,OZ;\n" \
        "Spain:                    14:  37:  EU:   40.37:     4.88:    -1.0:  EA:\n" \
        "    AM,AN,AO,EA,EB,EC,ED,EE,EF,EG,EH,=EA2EZ/P,=EA3HSD/P,=EA5CC/P,=EA5EZ/P,\n" \
        "    =EA8BFH/4,=EA8BFH/P,=EA9HU;\n" \
        "South Africa:             38:  57:  AF:  -29.07:   -22.63:    -2.0:  ZS:\n" \
        "    H5,S4,S8,V9,ZR,ZS,ZT,ZU,=ZS1CT/L,=ZS5ZLB/L;\n" \


        job=CtyImportJob()
        job.execute(content)


if __name__ == '__main__':
    unittest.main()