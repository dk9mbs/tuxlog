import unittest
import os
import config
from os import getenv
from model import model
from model.model import MySQLDatabase
from model.model import LogBands
from tuxlog.file_import.ctyimport import CtyImport
from tuxlog.band import frequency_to_band

class TestBand(unittest.TestCase):
    def test_band(self):
        config.DatabaseConfig.open(model.database, config.DatabaseConfig.read_from_file(os.getenv("tuxlog_environment")))

        print("\nBand:\n==============")

        band=frequency_to_band(14.074)
        print('Frequency => %s Band => %s' % (14.074, band.name))
        self.assertEqual(band.name, '20m')

        band=frequency_to_band(14.0)
        print('Frequency => %s Band => %s' % (14.0, band.name))
        self.assertEqual(band.name, '20m')

        band=frequency_to_band(14.35)
        print('Frequency => %s Band => %s' % (14.35, band.name))
        self.assertEqual(band.name, '20m')

        band=frequency_to_band(0.473)
        print('Frequency => %s Band => %s' % (0.473, band.name))
        self.assertEqual(band.name, '630m')

        band=frequency_to_band(241000.0)
        print('Frequency => %s Band => %s' % (241000.0, band.name))
        self.assertEqual(band.name, '1mm')
        
        band=frequency_to_band(13.0)
        print('Frequency => %s Band => %s' % (13.0, band))
        self.assertEqual(band, None)


if __name__ == '__main__':
    unittest.main()