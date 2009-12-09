import os.path
#!/usr/bin/python

##################
# fileID.py
#
# Copyright David Baddeley, 2009
# d.baddeley@auckland.ac.nz
#
# This file may NOT be distributed without express permision from David Baddeley
#
##################

import tables
import os

def genDataFileID(filename):
    h5f = tables.openFile(filename)

    ds = h5f.root.ImageData[0, :,:20].ravel()

    h5f.close()

    ds = ds - ds.mean()
    dss = ''.join(['%c' % (int(di + 128)) for di in ds])

    return hash(dss)


def genDataSourceID(datasource):
    ds = datasource.getSlice(0)[:,:20].ravel()

    ds = ds - ds.mean()
    dss = ''.join(['%c' % (int(di + 128)) for di in ds])

    return hash(dss)

def genResultsFileID(filename):
    h5f = tables.openFile(filename)

    ds = str(h5f.root.FitResults[0].data)

    h5f.close()

    return hash(ds)

def genFileID(filename):
    ext = os.path.splitext(filename)[1]

    if ext == 'h5':
        return genDataFileID(filename)
    elif ext = 'h5r':
        return genResultsFileID(filename)
    else:
        return None


def getImageID(filename):
    ext = os.path.splitext(filename)[1]

    if ext == 'h5':
        return genDataFileID(filename)
    elif ext = 'h5r':
        h5f = tables.openFile(filename)
        md = MetaDataHandler.HDFMDHandler(h5f)
        
        if 'Analysis.DataFileID' in md.getEntryNames():
            return md.getEntry('Analysis.DataFileID')
        else:
            return None

        h5f.close()
    else:
        return None

def guessH5RImageID(filename):
    #try and find the original data
    fns = filename.split(os.path.sep)
    cand = os.path.sep.join(fns[:-3]  + fns[-2:])[:-1]
    print cand
    if os.path.exists(cand):
        #print 'Found Analysis'
        return genResultsFileID(cand)
    else:
        return None




