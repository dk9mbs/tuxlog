import unittest
import config
import os
from model import model

class TestDxCallInfo(unittest.TestCase):

    def hook1(self, name, params, **kwargs):
        print('\nHallo aus 1 %s' % name)
        return True

    def hook2(self, name, params, **kwargs):
        print('\nHallo aus 2 %s' % name)
        return True

    def test_dxcallinfo(self):
        config.DatabaseConfig.open(model.database, config.DatabaseConfig.read_from_file(os.getenv("tuxlog_environment")))

        from usecases import app_hooks as hook

        hook.register('test', self.hook1 )
        hook.register('test', self.hook2 )
        hook.register('test2', self.hook1 )

        hook.execute('test', dict())
        hook.execute('test2', dict())


if __name__ == '__main__':
    unittest.main()

