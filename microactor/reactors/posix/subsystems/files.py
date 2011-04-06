import sys
from microactor.subsystems import Subsystem
from microactor.utils import Deferred
from ..transports.files import FileTransport, PipeTransport


class FilesSubsystem(Subsystem):
    NAME = "files"
    
    def _init(self):
        self.stdin = PipeTransport(self.reactor, sys.stdin, "r")
        self.stdout = PipeTransport(self.reactor, sys.stdout, "w")
        self.stderr = PipeTransport(self.reactor, sys.stderr, "w")
    
    def open(self, path, mode = "rt"):
        def opener():
            try:
                fileobj = open(path, mode)
            except Exception as ex:
                dfr.throw(ex)
                return
            mode2 = ""
            if "r" in mode or "+" in mode:
                mode2 += "r"
            if "a" in mode or "+" in mode:
                mode2 += "w"
            trns = FileTransport(self.reactor, fileobj, mode2)
            dfr.set(trns)
        
        dfr = Deferred()
        self.reactor.call(opener)
        return dfr


