# This file was created automatically by SWIG 1.3.29.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _sensicam
import new
new_instancemethod = new.instancemethod
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'PySwigObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0
del types


class CCamera(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CCamera, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CCamera, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _sensicam.new_CCamera(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _sensicam.delete_CCamera
    __del__ = lambda self : None;
    def GetCamType(*args): return _sensicam.CCamera_GetCamType(*args)
    def GetDataType(*args): return _sensicam.CCamera_GetDataType(*args)
    def GetADBits(*args): return _sensicam.CCamera_GetADBits(*args)
    def GetMaxDigit(*args): return _sensicam.CCamera_GetMaxDigit(*args)
    def GetNumberCh(*args): return _sensicam.CCamera_GetNumberCh(*args)
    def GetBytesPerPoint(*args): return _sensicam.CCamera_GetBytesPerPoint(*args)
    def GetCCDType(*args): return _sensicam.CCamera_GetCCDType(*args)
    def GetCamID(*args): return _sensicam.CCamera_GetCamID(*args)
    def GetCamVer(*args): return _sensicam.CCamera_GetCamVer(*args)
    def SetTrigMode(*args): return _sensicam.CCamera_SetTrigMode(*args)
    def GetTrigMode(*args): return _sensicam.CCamera_GetTrigMode(*args)
    def SetDelayTime(*args): return _sensicam.CCamera_SetDelayTime(*args)
    def GetDelayTime(*args): return _sensicam.CCamera_GetDelayTime(*args)
    def SetIntegTime(*args): return _sensicam.CCamera_SetIntegTime(*args)
    def GetIntegTime(*args): return _sensicam.CCamera_GetIntegTime(*args)
    def SetROIMode(*args): return _sensicam.CCamera_SetROIMode(*args)
    def GetROIMode(*args): return _sensicam.CCamera_GetROIMode(*args)
    def SetCamMode(*args): return _sensicam.CCamera_SetCamMode(*args)
    def GetCamMode(*args): return _sensicam.CCamera_GetCamMode(*args)
    def SetBoardNum(*args): return _sensicam.CCamera_SetBoardNum(*args)
    def GetBoardNum(*args): return _sensicam.CCamera_GetBoardNum(*args)
    def GetCCDWidth(*args): return _sensicam.CCamera_GetCCDWidth(*args)
    def GetCCDHeight(*args): return _sensicam.CCamera_GetCCDHeight(*args)
    def SetHorizBin(*args): return _sensicam.CCamera_SetHorizBin(*args)
    def GetHorizBin(*args): return _sensicam.CCamera_GetHorizBin(*args)
    def GetHorzBinValue(*args): return _sensicam.CCamera_GetHorzBinValue(*args)
    def SetVertBin(*args): return _sensicam.CCamera_SetVertBin(*args)
    def GetVertBin(*args): return _sensicam.CCamera_GetVertBin(*args)
    def GetNumberChannels(*args): return _sensicam.CCamera_GetNumberChannels(*args)
    def GetElectrTemp(*args): return _sensicam.CCamera_GetElectrTemp(*args)
    def GetCCDTemp(*args): return _sensicam.CCamera_GetCCDTemp(*args)
    def CamReady(*args): return _sensicam.CCamera_CamReady(*args)
    def GetPicWidth(*args): return _sensicam.CCamera_GetPicWidth(*args)
    def GetPicHeight(*args): return _sensicam.CCamera_GetPicHeight(*args)
    def SetROI(*args): return _sensicam.CCamera_SetROI(*args)
    def GetROIX1(*args): return _sensicam.CCamera_GetROIX1(*args)
    def GetROIX2(*args): return _sensicam.CCamera_GetROIX2(*args)
    def GetROIY1(*args): return _sensicam.CCamera_GetROIY1(*args)
    def GetROIY2(*args): return _sensicam.CCamera_GetROIY2(*args)
    def DisplayError(*args): return _sensicam.CCamera_DisplayError(*args)
    def Init(*args): return _sensicam.CCamera_Init(*args)
    def GetStatus(*args): return _sensicam.CCamera_GetStatus(*args)
    def SetCOC(*args): return _sensicam.CCamera_SetCOC(*args)
    def StartExposure(*args): return _sensicam.CCamera_StartExposure(*args)
    def StartLifePreview(*args): return _sensicam.CCamera_StartLifePreview(*args)
    def StopLifePreview(*args): return _sensicam.CCamera_StopLifePreview(*args)
    def ExpReady(*args): return _sensicam.CCamera_ExpReady(*args)
    def GetBWPicture(*args): return _sensicam.CCamera_GetBWPicture(*args)
    def ExtractColor(*args): return _sensicam.CCamera_ExtractColor(*args)
    def CheckCoordinates(*args): return _sensicam.CCamera_CheckCoordinates(*args)
CCamera_swigregister = _sensicam.CCamera_swigregister
CCamera_swigregister(CCamera)



