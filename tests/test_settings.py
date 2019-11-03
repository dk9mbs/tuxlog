import unittest
from model import model
from model.model import MySQLDatabase
from os import getenv
import os
import config
from tuxlog.system.setting import Setting


class TestSetting(unittest.TestCase):
    def test_get_setting(self):
        config.DatabaseConfig.open(model.database, config.DatabaseConfig.read_from_file(os.getenv("tuxlog_environment")))

        test=Setting.get_setting('dk9mbs','callbook_hamqth_password','g')
        self.assertEqual(test, 'password')

        test=Setting.get_setting('dk9mbs', 'default_power', '')
        self.assertEqual(test, '100')

        test=Setting.get_setting('dk9mbs', 'NOT_EXISTS_SETTING', 'xxx')
        self.assertEqual(test, 'xxx')

        test=Setting.get_setting('NOT_EXISTS_CALL', 'NOT_EXISTS_SETTING', 'xxx')
        self.assertEqual(test, 'xxx')

if __name__ == '__main__':
    unittest.main()