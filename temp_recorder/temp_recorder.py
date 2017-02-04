#!/usr/bin/env python3.5
import signal
import sys
import os
import time
import argparse
import logging

debug_p = False
def get_logger_name():
    return 'temp_recorder'

class TempRecorder:
    def _shut_down(self, lockf, exit_status = 0):
        self._release_lockfile(lockf)
        sys.exit(exit_status)
    
    def _grab_lockfile(self,lockf):
        fd = os.open(lockf,os.O_CREAT| os.O_EXCL)
    
    def _release_lockfile(self, lockf):
        try:
            os.remove(lockf)
        except:
            print("failed to release lock file.")
    
    def _read_temp(self, slave):
        tfile = open("/sys/bus/w1/devices/"+slave+"/w1_slave")
        text = tfile.read()
        tfile.close()
        secondline = text.split("\n")[1]
        temperaturedata = secondline.split(" ")[9]
        temperature = float(temperaturedata[2:])
        temperature = temperature / 1000
        return temperature
                                     
    def do_something(self, log):
        ### This does the "work" of the daemon
        #self._probe_id = "28-0000054823e9"
        while True:
            log("testing closure logger")
            time.sleep(5)
    
    def _setup_signals(self, lockf):
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
        this at anytime by just modifying _log_info here
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
        ### This launches the daemon in its context
    
        global debug_p
    
        try:
            self._grab_lockfile(lockf)
        except:
            print("failed to grab lock file, bailing...")
            sys.exit(0)
 
        self._setup_signals(lockf)
        log = self._setup_logger(logf)
    
        log("Temp_recorder daemon started.")
    
        if debug_p:
            print("temp_recorder: entered run()")
            print("temp_recorder: pidf = {}    logf = {}".format(pidf, logf))
            print("temp_recorder: about to start daemonization")
        self.do_something(log)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Example daemon in Python")
    parser.add_argument('-p', '--pid-file', default='/var/run/temp_recorder.pid')
    parser.add_argument('-l', '--log-file', default='/var/log/temp_recorder.log')
    parser.add_argument('-o', '--lock-file', default='/var/lock/temp_recorder')
    
    args = parser.parse_args()
    tr = TempRecorder()    
    tr.start_daemon(pidf=args.pid_file, logf=args.log_file, lockf=args.lock_file)

