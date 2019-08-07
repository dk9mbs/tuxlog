import unittest

from model import model
from model.model import MySQLDatabase
import json
from os import getenv


#from model import model
import config
environment=getenv("tuxlog_environment")
if environment==None or environment=="":
    environment="test"

config.DatabaseConfig.open(model.database, config.DatabaseConfig.read_from_file(environment))

class TestAdifImport(unittest.TestCase):
    def test_importadif(self):
        """
        Test that it can sum a list of integers
        """
        from usecases.adifimport import AdifImportLogic

        content = "WSJT-X ADIF Export<eoh>\n" \
        "<call:5>M0FLF <gridsquare:0> <mode:3>FT4 <rst_sent:3>+03 <rst_rcvd:3>-07 <qso_date:8>20190609 <time_on:6>170645 <qso_date_off:8>20190609 <time_off:6>170745 <band:3>20m <freq:9>14.075063 <station_callsign:6>DK9MBS <my_gridsquare:4>JO45 <tx_pwr:2>50 <STATE:0> <eor>\n" \
        "<call:6>2E0SMX <gridsquare:4>IO92 <mode:3>FT8 <rst_sent:3>-17 <rst_rcvd:3>-06 <qso_date:8>20190609 <time_on:6>171500 <qso_date_off:8>20190609 <time_off:6>171545 <band:3>20m <freq:9>14.075005 <station_callsign:6>DK9MBS <my_gridsquare:4>JO45 <tx_pwr:2>50 <eor>\n"

        parser = AdifImportLogic("LogLogs", "dk9mbs")
        @parser.register("after_save_adif_rec")
        def readline(**kwargs):
            #print("=========================START========================")
            #print("Test:"+str(kwargs['adif_rec'].__data__))
            #print("=========================END========================")
            pass

        @parser.register("error_save_adif_rec")
        def readlineerror(**kwargs):
            #print("=================START=EXCEPTION====================")
            #print("Test:"+str(kwargs['adif_rec'].__data__))
            #print("=========================END========================")
            pass
    
        parser.adif_import(content)


class TestAdifParser(unittest.TestCase):

    def test_adif_parser(self):
        from usecases.adifimport import AdifParserLib
        from model.model import MetaDataExchangeFields

        content = "WSJT-X ADIF Export<eoh>\n" \
        "<call:5>M0FLF <gridsquare:0> <mode:3>FT4 <rst_sent:3>+03 <rst_rcvd:3>-07 <qso_date:8>20190609 <time_on:6>170645 <qso_date_off:8>20190609 <time_off:6>170745 <band:3>20m <freq:9>14.075063 <station_callsign:6>DK9MBS <my_gridsquare:4>JO45 <tx_pwr:2>50 <STATE:0> <eor>\n" \
        "<call:6>2E0SMX <gridsquare:4>IO92 <mode:3>FT8 <rst_sent:3>-17 <rst_rcvd:3>-06 <qso_date:8>20190609 <time_on:6>171500 <qso_date_off:8>20190609 <time_off:6>171545 <band:3>20m <freq:9>14.075005 <station_callsign:6>DK9MBS <my_gridsquare:4>JO45 <tx_pwr:2>50 <eor>\n"

        @AdifParserLib
        def test(*args, **kwargs):
            adif=args[0]
            return {"band": adif['band'], "yourcall":adif['call']}

        result=test(content)
        self.assertEqual(dict(result[0])['band'], '20m')
        self.assertEqual(dict(result[0])['yourcall'], 'M0FLF')



if __name__ == '__main__':
    unittest.main()


