#!/usr/bin/env python3.5
from .context import temp_recorder
import unittest
import tempfile
import os


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_grab(self):
        '''
        a lockfile must not exist before grabbing
        '''
        tr = temp_recorder.TempRecorder()
        ntf = tempfile.NamedTemporaryFile(delete=False)
        try:
            tr._grab_lockfile(ntf.name)
            assert False
        except:
            assert True

    def test_release(self):
        '''
        a lockfile must not exist after being released
        '''
        tr = temp_recorder.TempRecorder()
        ntf = tempfile.NamedTemporaryFile(delete=False)
        tr._release_lockfile(ntf.name)
        assert not os.path.isfile(ntf.name)


    def test_grab_and_release(self):
        '''
        grabbing and releasing the lockfile works appropriately
        '''
        tr = temp_recorder.TempRecorder()
        
        ntf = tempfile.NamedTemporaryFile(delete=False)
        os.remove(ntf.name)
        assert not os.path.isfile(ntf.name)
        tr._grab_lockfile(ntf.name)
        assert os.path.isfile(ntf.name)
        tr._release_lockfile(ntf.name)
        assert not os.path.isfile(ntf.name)

    def test_logging(self):
        app_name = temp_recorder.get_logger_name()
        assert app_name == 'temp_recorder'


if __name__ == '__main__':
    import pdb
    pdb.set_trace()
    unittest.main()
