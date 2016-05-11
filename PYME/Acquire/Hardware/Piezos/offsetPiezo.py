# -*- coding: utf-8 -*-
"""
Created on Sat Sep 13 16:54:15 2014

@author: David Baddeley
"""
import Pyro.core
import Pyro.naming
import threading
from PYME.misc.computerName import GetComputerName

from PYME.Acquire import eventLog

#import Queue
#import time

class piezoOffsetProxy(Pyro.core.ObjBase):    
    def __init__(self, basePiezo):
        Pyro.core.ObjBase.__init__(self)
        self.basePiezo = basePiezo
        self.offset = 0
        #self.driftQueue = Queue.Queue()

    def ReInit(self):
        return self.basePiezo.ReInit()
        
    def SetServo(self,val = 1):
        return self.basePiezo.SetServo(val)
        
    def MoveTo(self, iChannel, fPos, bTimeOut=True):
        return self.basePiezo.MoveTo(iChannel, fPos + self.offset, bTimeOut)
            
    def MoveRel(self, iChannel, incr, bTimeOut=True):
        return self.basePiezo.MoveRel(iChannel, incr, bTimeOut)

    def GetPos(self, iChannel=0):
        return self.basePiezo.GetPos(iChannel) - self.offset
        
    def GetTargetPos(self, iChannel=0):
        return self.basePiezo.GetTargetPos(iChannel) - self.offset
        
    def GetControlReady(self):
        return self.basePiezo.GetControlReady()
         
    def GetChannelObject(self):
        return self.basePiezo.GetChannelObject()
        
    def GetChannelPhase(self):
        return self.basePiezo.GetChannelPhase()
        
    def GetMin(self,iChan=1):
        return self.basePiezo.GetMin(iChan)
        
    def GetMax(self, iChan=1):
        return self.basePiezo.GetMax(iChan)
        
    def GetFirmwareVersion(self):
        return self.basePiezo.GetFirmwareVersion()
        
    def GetOffset(self):
        return self.offset
        
    def SetOffset(self, val):
        p = self.GetPos()
        self.offset = val
        self.MoveTo(0, p)
        
    def LogShifts(self, dx, dy, dz):
        eventLog.logEvent('ShiftMeasure', '%3.4f, %3.4f, %3.4f' % (dx, dy, dz))
        #self.driftQueue.put((dx, dy, dz, time.time()))
        
        
class ServerThread(threading.Thread):
    def __init__(self, proxyPiezo):
        threading.Thread.__init__(self)
        
        compName = GetComputerName()
        
        Pyro.core.initServer()

        pname = "%s.Piezo" % compName
        
        try:
            from PYME.misc import pyme_zeroconf 
            ns = pyme_zeroconf.getNS()
        except:
            ns=Pyro.naming.NameServerLocator().getNS()

            if not compName in [n[0] for n in ns.list('')]:
                ns.createGroup(compName)

            #get rid of any previous instance
            try:
                ns.unregister(pname)
            except Pyro.errors.NamingError:
                pass        
        
        self.daemon=Pyro.core.Daemon()
        self.daemon.useNameServer(ns)
        
        self.piezo = proxyPiezo      

        #pname = "%s.Piezo" % compName
        
        
        
        uri=self.daemon.connect(self.piezo,pname)
        
    def run(self):
        print 'foo'
        #try:
        self.daemon.requestLoop()
        #finally:
        #    daemon.shutdown(True)
        
    def cleanup(self):
        print 'Shutting down Offset Piezo Server'
        self.daemon.shutdown(True)
                

def getClient(compName = GetComputerName()):
    try:
        from PYME.misc import pyme_zeroconf 
        ns = pyme_zeroconf.getNS()
        URI = ns.resolve('%s.Piezo' % compName)
    except:
        URI ='PYRONAME://%s.Piezo'%compName

    return Pyro.core.getProxyForURI(URI)
    
    
def main():
    '''For testing only'''
    from PYME.Acquire.Hardware.Simulator import fakePiezo
    bp = fakePiezo.FakePiezo(100)
    st = ServerThread(bp)
    print 'foo'
    st.start()
    st.join()
    #st.run()
    #st.daemon.requestLoop()
    print 'bar'
    
if __name__ == '__main__':
    main()