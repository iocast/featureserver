__author__  = "MetaCarta"
__copyright__ = "Copyright (c) 2006-2008 MetaCarta"
__license__ = "Clear BSD" 
__version__ = "$Id: __init__.py 498 2008-05-18 13:10:43Z crschmidt $"

import sys
import os
import warnings
import time


class Lock (object):
    """Locking method used in several DataSources which do not have
       internal locking mechanisms."""
    def __init__ (self, lock, timeout = 30.0, stale_interval = 300.0):
        self.lockfile = lock
        self.timeout  = float(timeout)
        self.stale    = float(stale_interval)

    def lock (self, blocking = True):
        result = self.attempt_lock()
        if result:
            return True
        elif not blocking:
            return False
        while result is not True:
            time.sleep(0.25)
            result = self.attempt_lock()
        return True

    def attempt_lock (self):
        try: 
            os.makedirs(self.lockfile)
            return True
        except OSError:
            pass
        try:
            status = os.stat(self.lockfile)
            if status.st_ctime + self.stale < time.time():
                warnings.warn("removing stale lock %s" % self.lockfile)
                # remove stale lock
                self.unlock()
                os.makedirs(self.lockfile)
                return True
        except OSError:
            pass
        return False 
     
    def unlock (self):
        try:
            os.rmdir(self.lockfile)
        except OSError, E:
            warnings.warn("unlock %s failed: %s" % (self.lockfile, str(E)))

    __del__ = unlock
