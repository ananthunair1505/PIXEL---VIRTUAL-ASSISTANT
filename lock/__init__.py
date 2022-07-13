from signal import getsignal, signal, SIGKILL, SIGINT, SIGTERM, \
    SIG_DFL, default_int_handler, SIG_IGN
import os
from microsoft.util import LOG
from microsoft.util.file_utils import get_temp_path
class Signal:
    def __init__(self, sig_value, func):
        super(Signal, self).__init__()
        self.__sig_value = sig_value
        self.__user_func = func
        self.__previous_func = signal(sig_value, self)
        self.__previous_func = {
            SIG_DFL: default_int_handler,
            SIG_IGN: lambda a, b: None
        }.get(self.__previous_func, self.__previous_func)
    def __call__(self, signame, sf):
        self.__user_func()
        self.__previous_func(signame, sf)
    def __del__(self):
        signal(self.__sig_value, self.__previous_func)
class Lock:
    DIRECTORY = get_temp_path('microsoft')
    FILE = '/{}.pid'
    def __init__(self, service):
        super(Lock, self).__init__()
        self.__pid = os.getpid()  
        self.path = Lock.DIRECTORY + Lock.FILE.format(service)
        self.set_handlers()
        self.create()
    def set_handlers(self):
        self.__handlers = {SIGINT: Signal(SIGINT, self.delete),
                           SIGTERM: Signal(SIGTERM, self.delete)}
    def exists(self):
        if not os.path.isfile(self.path):
            return
        with open(self.path, 'r') as L:
            try:
                os.kill(int(L.read()), SIGKILL)
            except Exception as E:
                pass
    def touch(self):
        if not os.path.exists(Lock.DIRECTORY):
            os.makedirs(Lock.DIRECTORY)
        with open(self.path, 'w') as L:
            L.write('{}'.format(self.__pid))
    def create(self):
        self.exists()
        self.touch()
    def delete(self, *args):
        try:
            with open(self.path, 'r') as L:
                pid = int(L.read())
                if self.__pid == pid:
                    os.unlink(self.path)
        except IOError:
            pass