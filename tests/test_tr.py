from .context import temp_recorder
import unittest
import tempfile
import os

class TestTrSuite(unittest.TestCase):
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
        tr = temp_recorder.TempRecorder()

        ntf = tempfile.NamedTemporaryFile(delete=False)
        app_name = temp_recorder.get_logger_name()
        log = tr._setup_logger(ntf.name)
        log_msg = "testing logger"
        log(log_msg)
        f = open(ntf.name)
        file_contents = f.read()
        assert log_msg in file_contents
        assert app_name in file_contents
        
    def test_read_temp(self):
        tr = temp_recorder.TempRecorder()
        
        example_contents_slave = "50 05 4b 46 7f ff 0c 10 1c : crc=1c YES\n50 05 4b 46 7f ff 0c 10 1c t=85000\n"
        ntf = tempfile.NamedTemporaryFile()
        tfile = open(ntf.name,'w')
        tfile.write(example_contents_slave)
        tfile.flush()
        
        temp = tr._read_temp(ntf.name)
        assert temp == 85.0

    
        
if __name__ == '__main__':
    unittest.main()
