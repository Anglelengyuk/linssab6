#################################################################
#                                                               #
#          SPEC MATHEMATICS                                     #
#                        version: a0.4                          #
# @author: Sergio Lins               sergio.lins@roma3.infn.it  #
#################################################################

import os
import numpy as np
import math
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import SpecRead
from PyMca5.PyMcaMath import SpecArithmetic as Arithmetic

NOISE = 80
FANO = 0.114

def DFT(fx):
    Fu = np.fft.fft(fx)
    Power = np.abs(Fu)**2
    FuFilt = np.fft.ifft(Fu)
    plt.plot(fx)
    plt.plot(FuFilt)
    plt.show()
    return FuFilt

def stacksum(firstspec,dimension):
    " DIMENSION STANDS FOR THE MAP DIMENSION, LINES*ROWS (OR THE NUMBER OF FILES) "
    " SO THE FUNCTION GETS THE TOTAL NUMBER OF SPECTRA TO BE STACKED "
    aux = SpecRead.getdata(firstspec)
    currentspectra = firstspec
    Stack = np.array([len(aux)])
    for i in range(dimension):
        spec = currentspectra
        data = np.asarray(SpecRead.getdata(spec))
        Stack = Stack + data
        currentspectra = SpecRead.updatespectra(spec,dimension)
    return Stack

def sigma(energy):
    return math.sqrt(((NOISE/2.3548)**2)+(3.85*FANO*energy))

def gaussianbuilder(channel,energy):
    sigma = sigma(energy)
    chEnergy = (channel*GAIN + B)*1000
    A = GAIN/(sigma)*math.sqrt(2*math.pi)
    return A*(math.exp(-(((energy-chEnergy)**2)/(2*(sigma**2)))))

def creategaussian(channels,energy):
    Gaussian = np.zeros([channels])
    if isinstance(energy,int):
        for i in range(channels):
            Gaussian[i]+=gaussianbuilder(i,energy)
    elif isinstance(energy,list): 
        for i in range(channels):
            for k in range(len(energy)):
                    Gaussian[i]+=gaussianbuilder(i,energy[k])
    return Gaussian

def getindex(value,array):
    ydata = array.tolist()
    return ydata.index(value)

def setROI(lookup,xarray,yarray):
    peak_corr = 0
#    print("---------------------------------------------")
    for peak_corr in range(2):
#        print("lookup: %d" % lookup)
        FWHM = 2.3548 * sigma(lookup)
        lowx = (lookup - (FWHM))/1000
        highx = (lookup + (FWHM))/1000
#        print("FWHM: %f\nlowx: %f\nhighx: %f" % (FWHM, lowx,highx))
        idx = 0
        while xarray[idx] <= lowx:
            idx+=1
        lowx_idx = idx-1
#        print("lowx_idx: %d" % lowx_idx)
        while xarray[idx] <= highx:
            idx+=1
        highx_idx = idx-1
        ROI = xarray[lowx_idx:highx_idx]
        data = yarray[lowx_idx:highx_idx]
        ROI = np.asarray(ROI)
        data = np.asarray(data)
        shift = Arithmetic.search_peak(ROI,data)
        lookup = shift[0]*1000
#        print("iteration: %d PEAK MAX: %f" % (peak_corr,lookup))
#        print(ROI[0],ROI[-1])
#    plt.plot(xarray,yarray)
#    plt.plot(ROI,data)
#    plt.show()
    return lowx_idx,highx_idx

def getpeakarea(file,lookup,energyaxis):
    Area = 0
    data = SpecRead.getdata(file)
    idx = setROI(lookup,energyaxis,data)
    xdata = energyaxis[idx[0]:idx[1]]
    ydata = data[idx[0]:idx[1]]
    for i in range(len(xdata)):
        Area += ydata[i]
    return Area

if __name__=="__main__":

    file = SpecRead.input
    calibration = SpecRead.calibrate(file,'data')
    GAIN = calibration[-1]/len(calibration)
    B = calibration[0]
