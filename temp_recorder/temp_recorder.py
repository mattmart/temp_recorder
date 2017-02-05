import signal
import sys
import os
import time
import argparse
import logging

def get_logger_name():
    return 'temp_recorder'
 
class TempRecorder:

   
    def _shut_down(self, lockf, exit_status = 0):
        '''
        release and clean up all lock/log files here
        and exit with whatever status is necessary
        '''
        self._release_lockfile(lockf)
        sys.exit(exit_status)
    
    def _grab_lockfile(self,lockf):
        '''
        atomically creates a file after ensuring 
        it doesn't exist (if you're not familiar
        with os flags, man open)
        '''
        fd = os.open(lockf,os.O_CREAT| os.O_EXCL)
    
    def _release_lockfile(self, lockf):
        '''
        analogue of grab_lockfile. Doesn't currently
        do anything fancy except delete the file
        '''
        try:
            os.remove(lockf)
        except:
            print("failed to release lock file.")
    
    def _read_temp(self, w1_slave):
        '''
        reads a file (example contents contained in tests)
        and pulls out the temperature (assumes Celsius)
        and returns it to the caller. Does touch disk, 
        be careful
        '''
        tfile = open(w1_slave)
        text = tfile.read()
        tfile.close()
        secondline = text.split("\n")[1]
        temperaturedata = secondline.split(" ")[9]
        temperature = float(temperaturedata[2:])
        temperature = temperature / 1000
        return temperature
                                     
    def do_something(self, log):
        '''
        the main heart of the daemon. This is
        where we'll loop forever reading the temp
        and reporting it to wherever we decide
        '''
        while True:
            log("testing closure logger")
            time.sleep(5)
            #"/sys/bus/w1/devices/"+slave+"/w1_slave"
            #self._probe_id = "28-0000054823e9"

    
    def _setup_signals(self, lockf):
        '''
        sets up cleaning up the lock file
        and the logfile whenever SIGTERM or 
        SIGINT received
        
        not sure how to test installing signals...
        '''
        def __signal_handler(signal, frame):
            self._shut_down(lockf)
        
        signal.signal(signal.SIGINT, __signal_handler)
        signal.signal(signal.SIGTERM, __signal_handler)
    
       
    def _setup_logger(self, logf):
        '''
        This is a bit confusing so it deserves a comment.
        This is basically returning a logger that's set up
        how we want it - we want to log to our own 
        independent logger (note: we can change
        this at anytime by just modifying _log_info here.
        for example, if you wanted to start logging to
        syslog in addition to the log file, just import 
        syslog and syslog.notice inside _log_info)
        '''
        logger = logging.getLogger(get_logger_name())
        logger.setLevel(logging.INFO)
        
        fh = logging.FileHandler(logf)
        fh.setLevel(logging.INFO)
        
        formatstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(formatstr)
        
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
        def _log_info(msg):
            logger.info(msg)
    
        return _log_info
        
    def start_daemon(self, pidf, logf, lockf):
        '''
        starts up the daemon with the log/lockfiles
        this runs forever if it can grab the lockfile
        until given sigint/sigterm

        This method is a bit untestable, what with the 
        running forever and sys exit business. Anything
        added here should have other test coverage
        '''
    
        try:
            self._grab_lockfile(lockf)
        except:
            print("failed to grab lock file, bailing...")
            sys.exit(0)
 
        self._setup_signals(lockf)
        log = self._setup_logger(logf)
    
        log("Temp_recorder daemon started.")
        self.do_something(log)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Example daemon in Python")
    parser.add_argument('-p', '--pid-file', default='/var/run/temp_recorder.pid')
    parser.add_argument('-l', '--log-file', default='/var/log/temp_recorder.log')
    parser.add_argument('-o', '--lock-file', default='/var/lock/temp_recorder')
    
    args = parser.parse_args()
    tr = TempRecorder()
    tr.start_daemon(pidf=args.pid_file, logf=args.log_file, lockf=args.lock_file)

