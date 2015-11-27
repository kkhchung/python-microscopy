# -*- coding: utf-8 -*-
"""
Created on Mon May 25 17:15:01 2015

@author: david
"""

from .base import ModuleBase, register_module, Filter, Float, Enum, CStr, Bool, Int, View, Item, Group, File
import numpy as np
from scipy import ndimage
from PYME.DSView.image import ImageStack

@register_module('SimpleThreshold') 
class SimpleThreshold(Filter):
    threshold = Float(0.5)
    
    def applyFilter(self, data, chanNum, frNum, im):
        mask = data > self.threshold
        return mask

    def completeMetadata(self, im):
        im.mdh['Processing.SimpleThreshold'] = self.threshold
 
@register_module('Label')        
class Label(Filter):
    minRegionPixels = Int(10)
    
    def applyFilter(self, data, chanNum, frNum, im):
        mask = data > 0.5
        labs, nlabs = ndimage.label(mask)
        
        rSize = self.minRegionPixels
        
        if rSize > 1:
            m2 = 0*mask
            objs = ndimage.find_objects(labs)
            for i, o in enumerate(objs):
                r = labs[o] == i+1
                #print r.shape
                if r.sum() > rSize:
                    m2[o] = r
                                
            labs, nlabs = ndimage.label(m2)
            
        return labs

    def completeMetadata(self, im):
        im.mdh['Labelling.MinSize'] = self.minRegionPixels
        
@register_module('SelectLabel') 
class SelectLabel(Filter):
    '''Creates a mask corresponding to all pixels with the given label'''
    label = Int(1)
    
    def applyFilter(self, data, chanNum, frNum, im):
        mask = (data == self.label)
        return mask

    def completeMetadata(self, im):
        im.mdh['Processing.SelectedLabel'] = self.label

@register_module('LocalMaxima')         
class LocalMaxima(Filter):
    threshold = Float(.3)
    minDistance = Int(10)
    
    def applyFilter(self, data, chanNum, frNum, im):
        import skimage.feature
        im = data.astype('f')/data.max()
        return skimage.feature.peak_local_max(im, threshold_abs = self.threshold, min_distance = self.minDistance, indices=False)

    def completeMetadata(self, im):
        im.mdh['LocalMaxima.threshold'] = self.threshold
        im.mdh['LocalMaxima.minDistance'] = self.minDistance
        
@register_module('SVMSegment')         
class svmSegment(Filter):
    classifier = File('')
    
    def _loadClassifier(self):
        from PYME.Analysis import svmSegment
        if not '_cf' in dir(self):
            self._cf = svmSegment.svmClassifier(filename=self.classifier)
    
    def applyFilter(self, data, chanNum, frNum, im):
        self._loadClassifier()
        
        return self._cf.classify(data.astype('f'))

    def completeMetadata(self, im):
        im.mdh['SVMSegment.classifier'] = self.classifier
        

        

@register_module('Deconvolve')         
class Deconvolve(Filter):
    offset = Float(0)
    method = Enum('Richardson-Lucy', 'ICTM') 
    iterations = Int(10)
    psfType = Enum('file', 'bead', 'Lorentzian')
    psfFilename = CStr('') #only used for psfType == 'file'
    lorentzianFWHM = Float(50.) #only used for psfType == 'Lorentzian'
    beadDiameter = Float(200.) #only used for psfType == 'bead'
    regularisationLambda = Float(0.1) #Regularisation - ICTM only
    padding = Int(0) #how much to pad the image by (to reduce edge effects)
    zPadding = Int(0) # padding along the z axis
    
    _psfCache = {}
    _decCache = {}
    
    view = View(Item(name='inputName'),
                Item(name='outputName'),
                Item(name='processFramesIndividually'),
                Group(Item(name='method'),
                      Item(name='iterations'),
                      Item(name='offset'),
                      Item(name='padding'),
                      Item(name='zPadding'),
                      Item(name='regularisationLambda', visible_when='method=="ICTM"'),
                      label='Deconvolution Parameters'),
                Group(Item(name='psfType'),
                      Item(name='psfFilename', visible_when='psfType=="file"'),
                      Item(name='lorentzianFWHM', visible_when='psfType=="Lorentzian"'),
                      Item(name='beadDiameter', visible_when='psfType=="bead"'),
                      label='PSF Parameters'),
                resizable = True,
                buttons   = [ 'OK' ])
                

    
    def GetPSF(self, vshint):
        psfKey = (self.psfType, self.psfFilename, self.lorentzianFWHM, self.beadDiameter, vshint)
        
        if not psfKey in self._psfCache.keys():
            if self.psfType == 'file':
                psf, vs = np.load(self.psfFilename)
                psf = np.atleast_3d(psf)
                
                vsa = 1e3*np.array([vs.x, vs.y, vs.z]) 
                
                if not np.allclose(vshint, vsa, rtol=.03):
                    psf = ndimage.zoom(psf, vshint/vsa)
                
                self._psfCache[psfKey] = (psf, vs)        
            elif (self.psfType == 'Lorentzian'):
                from scipy import stats
                sc = self.lorentzianFWHM/2.0
                X, Y = np.mgrid[-30.:31., -30.:31.]
                R = np.sqrt(X*X + Y*Y)
                
                if not vshint is None:
                    vx = vshint[0]
                else:
                    vx = sc/2.
                
                vs = type('vs', (object,), dict(x=vx/1e3, y=vx/1e3))
                
                psf = np.atleast_3d(stats.cauchy.pdf(vx*R, scale=sc))
                    
                self._psfCache[psfKey] = (psf/psf.sum(), vs)
            elif (self.psfType == 'bead'):
                from PYME.Deconv import beadGen
                psf = beadGen.genBeadImage(self.beadDiameter/2, vshint)
                
                vs = type('vs', (object,), dict(x=vshint[0]/1e3, y=vshint[1]/1e3))
                
                self._psfCache[psfKey] = (psf/psf.sum(), vs)
                
                
        return self._psfCache[psfKey]
        
    def GetDec(self, dp, vshint):
        '''Get a (potentially cached) deconvolution object'''
        from PYME.Deconv import dec, richardsonLucy
        decKey = (self.psfType, self.psfFilename, self.lorentzianFWHM, self.beadDiameter, vshint, dp.shape, self.method)
        
        if not decKey in self._decCache.keys():
            psf = self.GetPSF(vshint)[0]
            
            #create the right deconvolution object
            if self.method == 'ICTM':
                if self.psfType == 'bead':
                    dc = dec.dec_bead()
                else:
                    dc = dec.dec_conv()
            else:
                if self.psfType == 'bead':
                    dc = richardsonLucy.rlbead()
                else:
                    dc = richardsonLucy.dec_conv()
                    
            #resize the PSF to fit, and do any required FFT planning etc ...
            dc.psf_calc(psf, dp.shape)
            
            self._decCache[decKey] = dc
            
        return self._decCache[decKey]
            
    
    def applyFilter(self, data, chanNum, frNum, im):
        d = np.atleast_3d(data.astype('f') - self.offset)
        #vx, vy, vz = np.array(im.voxelsize)*1e-3
        
        #Pad the data (if desired)
        if self.padding > 0:
            padsize = np.array([self.padding, self.padding, self.zPadding])
            dp = np.ones(np.array(d.shape) + 2*padsize, 'f')*d.mean()
            weights = np.zeros_like(dp)
            px, py, pz = padsize

            dp[px:-px, py:-py, pz:-pz] = d
            weights[px:-px, py:-py, pz:-pz] = 1.
            weights = weights.ravel()
        else: #no padding
            dp = d
            weights = 1
            
        #psf, vs = self.GetPSF(im.voxelsize)
        
        #Get appropriate deconvolution object        
        dec = self.GetDec(dp, im.voxelsize)
        
        #run deconvolution
        res = dec.deconv(dp, self.regularisationLambda, self.iterations, weights).reshape(dec.shape)
        
        #crop away the padding
        if self.padding > 0:
            res = res[px:-px, py:-py, pz:-pz]
        
        return res

    def completeMetadata(self, im):
        im.mdh['Deconvolution.Offset'] = self.offset
        im.mdh['Deconvolution.Method'] = self.method
        im.mdh['Deconvolution.Iterations'] = self.iterations
        im.mdh['Deconvolution.PsfType'] = self.psfType
        im.mdh['Deconvolution.PSFFilename'] = self.psfFilename
        im.mdh['Deconvolution.LorentzianFWHM'] = self.lorentzianFWHM
        im.mdh['Deconvolution.BeadDiameter'] = self.beadDiameter
        im.mdh['Deconvolution.RegularisationLambda'] = self.regularisationLambda
        im.mdh['Deconvolution.Padding'] = self.padding
        im.mdh['Deconvolution.ZPadding'] = self.zPadding
        

    
@register_module('DistanceTransform')     
class DistanceTransform(Filter):    
    def applyFilter(self, data, chanNum, frNum, im):
        mask = 1.0*(data > 0.5)
        voxelsize = np.array(im.voxelsize)[:mask.ndim]
        dt = -ndimage.distance_transform_edt(data, sampling=voxelsize)
        dt = dt + ndimage.distance_transform_edt(ndimage.binary_dilation(1-mask), sampling=voxelsize)
        return dt

@register_module('BinaryDilation')      
class BinaryDilation(Filter):
    iterations = Int(1)
    radius = Float(1)
    
    def applyFilter(self, data, chanNum, frNum, im):
        import skimage.morphology
        
        if len(data.shape) == 3: #3D
            selem = skimage.morphology.ball(self.radius)
        else:
            selem = skimage.morphology.disk(self.radius)
        return ndimage.binary_dilation(data, selem)

@register_module('BinaryErosion')         
class BinaryErosion(Filter):
    iterations = Int(1)
    radius = Float(1)
    
    def applyFilter(self, data, chanNum, frNum, im):
        import skimage.morphology
        
        if len(data.shape) == 3: #3D
            selem = skimage.morphology.ball(self.radius)
        else:
            selem = skimage.morphology.disk(self.radius)
        return ndimage.binary_erosion(data, selem)

@register_module('BinaryFillHoles')         
class BinaryFillHoles(Filter):
    iterations = Int(1)
    radius = Float(1)
    
    def applyFilter(self, data, chanNum, frNum, im):
        import skimage.morphology
        
        if len(data.shape) == 3: #3D
            selem = skimage.morphology.ball(self.radius)
        else:
            selem = skimage.morphology.disk(self.radius)
        return ndimage.binary_fill_holes(data, selem)

@register_module('Watershed')         
class Watershed(ModuleBase):
    '''Module with one image input and one image output'''
    inputImage = CStr('input')
    inputMarkers = CStr('markers')
    inputMask = CStr('')
    outputName = CStr('watershed')
    
    processFramesIndividually = Bool(False)
    
    def filter(self, image, markers, mask=None):
        if self.processFramesIndividually:
            filt_ims = []
            for chanNum in range(image.data.shape[3]):
                if not mask == None:
                    filt_ims.append(np.concatenate([np.atleast_3d(self.applyFilter(image.data[:,:,i,chanNum].squeeze(), markers.data[:,:,i,chanNum].squeeze(), mask.data[:,:,i,chanNum].squeeze())) for i in range(image.data.shape[2])], 2))
                else:
                    filt_ims.append(np.concatenate([np.atleast_3d(self.applyFilter(image.data[:,:,i,chanNum].squeeze(), markers.data[:,:,i,chanNum].squeeze())) for i in range(image.data.shape[2])], 2))
        else:
            if not mask == None:
                filt_ims = [np.atleast_3d(self.applyFilter(image.data[:,:,:,chanNum].squeeze(), markers.data[:,:,:,chanNum].squeeze(), mask.data[:,:,:,chanNum].squeeze())) for chanNum in range(image.data.shape[3])]
            else:
                filt_ims = [np.atleast_3d(self.applyFilter(image.data[:,:,:,chanNum].squeeze(), mask.data[:,:,:,chanNum].squeeze())) for chanNum in range(image.data.shape[3])]
            
        im = ImageStack(filt_ims, titleStub = self.outputName)
        im.mdh.copyEntriesFrom(image.mdh)
        im.mdh['Parent'] = image.filename
        
        #self.completeMetadata(im)
        
        return im
        
    def applyFilter(self, image,markers, mask=None):
        import skimage.morphology

        img = ((image/image.max())*2**15).astype('int16')         
        
        if not mask is None:
            return skimage.morphology.watershed(img, markers.astype('int16'), mask = mask.astype('int16'))
        else:
            return skimage.morphology.watershed(img, markers.astype('int16'))
        
    def execute(self, namespace):
        image = namespace[self.inputImage]
        markers =  namespace[self.inputMarkers]
        if self.inputMask in ['', 'none', 'None']:
            namespace[self.outputName] = self.filter(image, markers)
        else:
            mask = namespace[self.inputMask]
            namespace[self.outputName] = self.filter(image, markers, mask)




        