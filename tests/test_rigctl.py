import unittest
from usecases.rigctl import RigCtl



class TestRigCtl(unittest.TestCase):
    cfg={"host":"127.0.0.1", "port":4532}

    # begin of mock
    class MockRig:
        def __init__(self, answer):
            self._answer=answer

        def close(self):
            pass

        def send(self, command):
            pass

        def recv(self, size):
            return bytes(self._answer+"\n", 'UTF-8')

    # end of mock

    def test_set_rig(self):

        #correct result
        response=RigCtl(self.cfg, mock=TestRigCtl.MockRig('RPRT 0')).set_rig("F", ['27000000'])
        print ("\nResponse set => "+response)

        # wrong result
        try:
            response=RigCtl(self.cfg, mock=TestRigCtl.MockRig('0')).set_rig("F", ['28000000'])
            print ("\nResponse set => "+response)
            raise Exception('TEST Error: no errorwas arraised ...')
        except Exception:
            print ("error arraised ... because the answer has a wrong format!")
        pass

    def test_get_rig(self):
        # retrieve an parameter from rig        
        

        response=RigCtl(self.cfg, mock=TestRigCtl.MockRig('get_mode:\nMode: FM\nPassband: 15000\nRPRT 0')).get_rig("m")
        print ("Response get => "+str(response))
        pass




if __name__ == '__main__':
    unittest.main()