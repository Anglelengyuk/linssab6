#################################################################
#                                                               #
#          SPEC READER                                          #
#                        version: 0.0.2α                        #
# @author: Sergio Lins               sergio.lins@roma3.infn.it  #
#################################################################

import logging
from ReadConfig import unpack_cfg as CONFIGURE
from ReadConfig import pop_error
logging.debug("Importing module SpecRead.py...")
import sys
import os
import time
import numpy as np
import matplotlib.pyplot as plt
logging.debug("Finished SpecRead imports.")

def get_samples_folder(inifile):
    ini = open(inifile,"r")
    folder = ini.readline()
    ini.close() 
    return folder

samples_folder = get_samples_folder(os.getcwd()+"\\folder.ini")
logging.info("Samples path: {0}".format(samples_folder))

def findprefix():
    mca_prefix = 'None'
    files = [name for name in os.listdir(selected_sample_folder)]
    for item in range(len(files)): 
        try:
            files[item] = files[item].split("_",1)[0]
        except: pass
    counter = dict((x,files.count(x)) for x in files)
    mca_prefix_count = 0
    for counts in counter:
        if counter[counts] > mca_prefix_count:
            mca_prefix = counts
            mca_prefix_count = counter[counts]
    if os.path.exists(selected_sample_folder+mca_prefix+'_1.mca'): 
        firstfile_path = selected_sample_folder+mca_prefix+'_1.mca'
    elif os.path.exists(selected_sample_folder+mca_prefix+'_1.txt'): 
        firstfile_path = selected_sample_folder+mca_prefix+'_1.txt'
    else: raise IOError("No mca or txt file with prefix {1} found in directory {0}".\
            format(selected_sample_folder,mca_prefix))
    return firstfile_path

def getfirstfile():
    return FIRSTFILE_ABSPATH

def setup():
    
    # reads config.cfg file and sets up the configuration according to what is
    # contained there

    global CONFIG, CALIB, DIRECTORY, samples_folder, selected_sample_folder, workpath, cube_path, output_path, dimension_file, FIRSTFILE_ABSPATH, global_list
    CONFIG,CALIB = CONFIGURE()
    DIRECTORY = CONFIG.get('directory')
    selected_sample_folder = samples_folder + DIRECTORY + '\\'
    workpath = os.getcwd()
    cube_path = workpath+'\output\\'+DIRECTORY+'\\'+DIRECTORY+'.cube'
    output_path = workpath+'\output\\'+DIRECTORY+'\\'
    dimension_file = selected_sample_folder + '\colonneXrighe.txt'
    try: FIRSTFILE_ABSPATH = findprefix()
    except: FIRSTFILE_ABSPATH = selected_sample_folder+'void.mca'
    global_list =  [CONFIG, CALIB, DIRECTORY, samples_folder, selected_sample_folder, workpath, cube_path, output_path, dimension_file, FIRSTFILE_ABSPATH]
    return np.nan

def setup_from_datacube(datacube,sample_database):
    
    # setup the configuration according to what is built into the datacube

    global CONFIG, CALIB, DIRECTORY, samples_folder, selected_sample_folder, workpath, cube_path, output_path, dimension_file, FIRSTFILE_ABSPATH, global_list
    
    CONFIG,CALIB = datacube.config, datacube.calibration
    DIRECTORY = CONFIG.get('directory')
    selected_sample_folder = samples_folder + DIRECTORY + '\\'
    workpath = os.getcwd()
    cube_path = workpath+'\output\\'+DIRECTORY+'\\'+DIRECTORY+'.cube'
    output_path = workpath+'\output\\'+DIRECTORY+'\\'
    dimension_file = selected_sample_folder + '\colonneXrighe.txt'
    
    try: FIRSTFILE_ABSPATH = sample_database[DIRECTORY]
    except: FIRSTFILE_ABSPATH = selected_sample_folder+'void.mca'
    
    global_list =  [CONFIG, CALIB, DIRECTORY,
            samples_folder, selected_sample_folder, workpath,
            cube_path, output_path, dimension_file,
            FIRSTFILE_ABSPATH]
    return np.nan 

def conditional_setup(name='None'):
    logging.debug("Running conditional setup for {}".format(name)) 
    # reads the config file but changes the directory to the sample_name variable
    # before setting up the PATHS
    
    global CONFIG, CALIB, DIRECTORY, samples_folder, selected_sample_folder, workpath, cube_path, output_path, dimension_file, FIRSTFILE_ABSPATH, global_list
    
    
    CONFIG,CALIB = CONFIGURE()
    CONFIG['directory'] = name
    DIRECTORY = CONFIG.get('directory')
    selected_sample_folder = samples_folder + DIRECTORY + '\\'
    workpath = os.getcwd()
    cube_path = workpath+'\output\\'+DIRECTORY+'\\'+DIRECTORY+'.cube'
    output_path = workpath+'\output\\'+DIRECTORY+'\\'
    dimension_file = selected_sample_folder + '\colonneXrighe.txt'
    
    FIRSTFILE_ABSPATH = selected_sample_folder + "\\" + name

    global_list =  [CONFIG, CALIB, DIRECTORY,
            samples_folder, selected_sample_folder, workpath,
            cube_path, output_path, dimension_file]
    
    return np.nan

def RatioMatrixReadFile(ratiofile):
    MatrixArray = []
    with open (ratiofile,'rt') as in_file:
        for line in in_file:
            MatrixArray.append(line.strip("\n"))
        for i in range(len(MatrixArray)): 
            MatrixArray[i] = MatrixArray[i].split()
        for j in range(len(MatrixArray)):
            for k in range(len(MatrixArray[j])):
                if MatrixArray[j][k].isdigit() == True: MatrixArray[j][k]=int(MatrixArray[j][k])
                else: MatrixArray[j][k]=1
        if len(MatrixArray[-1]) == 0: MatrixArray[-1]=[1, 1, 1, 1]
    MatrixArray = np.asarray(MatrixArray)
    iterx=0
    itery=0
    
    for i in range(len(MatrixArray)):
        if len(MatrixArray[i]) > 1:
            if MatrixArray[i][0] > 0\
                    and MatrixArray[i][0] > MatrixArray[i-1][0]\
                    and MatrixArray[i][0] > iterx: iterx=int(MatrixArray[i][0])
        if len(MatrixArray[i]) > 1:
            if MatrixArray[i][1] > 0\
                    and MatrixArray[i][1] > MatrixArray[i-1][1]\
                    and MatrixArray[i][1] > itery: itery=int(MatrixArray[i][1])

    RatesMatrix=np.zeros((iterx+1,itery+1))
    for i in range(len(MatrixArray)):
        x=int(MatrixArray[i][0])
        y=int(MatrixArray[i][1])
        ka=int(MatrixArray[i][2])
        kb=int(MatrixArray[i][3])
        if kb == 0: ka,kb = 0,1
        RatesMatrix[x,y] = ka/kb
        if ka/kb > 15: RatesMatrix[x,y] = 0  # CUTOFF FILTER FOR PEAK ERRORS #
    return RatesMatrix

def getheader(mca):
    ObjectHeader=[]
    specile = open(mca)
    line = specfile.readline()
    while "<<DATA>>" not in line:
        ObjectHeader.append(line.replace('\n',' '))
        line = specfile.readline()
        if "<<CALIBRATION>>" in line:
            specfile.close()
            break
    return ObjectHeader

def getcalibration():
    if CONFIG['calibration'] == 'manual':
        param = CALIB 
    elif CONFIG['calibration'] == 'from_source':
        param = []
        mca_file = open(getfirstfile(),'r')
        line = mca_file.readline()
        while line != "":
            while "<<CALIBRATION>>" not in line:
                line = mca_file.readline()
                if line == "": break
            while "<<DATA>>" not in line:
                line = mca_file.readline()
                if line == "": break
                line=line.replace('\r','')
                line=line.replace('\n','')
                line=line.replace('\t',' ')
                aux = line.split()
                try: param.append([int(aux[0]),float(aux[1])])
                except: pass 
            line = mca_file.readline()
        mca_file.close()
        if param == []: 
            pop_error("Calibration Error","Could not fetch calibration from source! Retry with manual calibration")
            raise ValueError("Couldn't fetch calibration from source!")
        for parameter in param:
            if len(param) <= 1: 
                pop_error("Calibration Error","Need at least two calibration points!")
                raise ValueError("Need at least two calibration points!")
            elif parameter[0] < 0 or parameter[1] < 0: 
                pop_error("Calibration Error","Can't receive negative values!")
                raise ValueError("Cant receive negative values!")
            elif parameter[0] == 0 or parameter[1] == 0:
                pop_error("Calibration Error","Can't receive zero as parameter!")
                raise ValueError("Cant receive zero as parameter!")
        else: pass
    else: 
        raise ValueError("Calibration mode {0} unknown! Check config.cfg")
    return param

def getdata(mca):
    name = str(mca)
    name = name.replace('_',' ')
    name = name.replace('\\',' ')
    name = name.split()
    # custom MC generated files
    if 'test' in name or 'obj' in name or 'newtest' in name:
        Data = []
        datafile = open(mca)
        lines = datafile.readlines()
        for line in lines:
            line = line.split()
            counts = float(line[1])
            counts = counts * 10e3
            Data.append(counts)
        Data = np.asarray(Data)

    # this works for the mca files
    else:
        ObjectData=[]
        datafile = open(mca)
        line = datafile.readline()
        while "<<DATA>>" not in line:
            line = datafile.readline()
            if line == "": break
        line = datafile.readline()
        while "<<END>>" not in line:
            try: ObjectData.append(int(line))
            except: 
                logging.warning("Mca file {} could not be read.".format(mca))
                datafile.close()
                return mca
            line = datafile.readline()
            if line == "": break
        Data = np.asarray(ObjectData)
    datafile.close()
    return Data

def calibrate():
    
    """
    Returns the energy axis and gain of the calibrated axis
    The parameter are taken from config.cfg is calibration is set to manual
    or from the mca files is calibration is set to from_source
    
    """
    param = getcalibration()
    x=[]
    y=[]
    for i in range(len(param)):
        for k in range(len(param[i])):
            x.append(param[i][0])
            y.append(param[i][1])
    x=np.asarray([x])
    y=np.asarray([y])
    coefficients=list(linregress(x,y))
    GAIN=coefficients[0]
    B=coefficients[1]
    R=coefficients[2]
    logging.info("Correlation coefficient R = %f!" % R)
    n = len(getdata(getfirstfile()))
    curve = []
    for i in range(n):
        curve.append((GAIN*i)+B)
    curve = np.asarray(curve)
    return curve,GAIN

def getgain():
    calibration = calibrate()
    curve = calibration[0]
    n = len(curve)
    GAIN=0
    for i in range(n-1):
        GAIN+=curve[i+1]-curve[i]
    return GAIN/n

def getsum(mca):
    DATA = getdata(mca)
    SUM = 0
    for i in range(len(DATA)):
        SUM+=DATA[i]
    return SUM

def getplot(mca):
    calibration = calibrate(mca,'file')
    energy = calibration[1]
    data=getdata(mca)
    plt.plot(energy,data)
    plt.show()
    return 0
   
def updatespectra(specfile,size):
    name=str(specfile)
    name=name.replace('_',' ')
    name=name.replace('.',' ')
    name=name.split()
    for i in range(len(name)):
        if name[i].isdigit()==True: index=int(name[i])
        if name[i] == "mca": extension=name[i]
        elif name[i] == "txt": extension=name[i]
        if len(name[i]) > 6: prefix = name[i]
    if index < size: index = str(index+1)
    else: index = str(size)
    newfile = str(prefix+'_'+index+'.'+extension)
    return newfile

def getdimension():
    if not os.path.exists(dimension_file):
        try: local_file = output_path + "colonneXrighe.txt"
        except:
            raise IOError("Dimension file not found!") 
    else: local_file = dimension_file
    user_input = False
    dm_file = open(local_file, 'r')
    line = dm_file.readline()
    if 'righe' in line:
        line=line.replace('\r','')
        line=line.replace('\n','')
        line=line.replace('\t',' ')
        aux = line.split()
        x = int(aux[1])
        line = dm_file.readline() 
    if 'colonne' in line:
        line=line.replace('\r','')
        line=line.replace('\n','')
        line=line.replace('\t',' ')
        aux = line.split()
        y = int(aux[1])
        line = dm_file.readline() 
    while line != "":
        if line.startswith("*"): user_input = True
        line = dm_file.readline()
    dm_file.close()
    return x,y,user_input

def dump_ratios(maps_list,element_list):
    # this is to work with multiprocessing Mapping mode
    
    ratiofiles = ['' for x in range(len(element_list))]
    for Element in range(len(element_list)): 
        ratiofiles[Element] = str(output_path+\
                '{1}_ratio_{0}.txt'.format(element_list[Element],DIRECTORY))
        r_file = open(ratiofiles[Element],'w+')
        r_file.readline()
        r_file.truncate()
        r_file.write("-"*10 + " Counts of Element {0} "\
                .format(element_list[Element]) + 10*"-" + '\n')
        r_file.write("row\tcolumn\tline1\tline2\tratio\n")
        r_file.close() 

    for Element in range(len(element_list)):
        r_file = open(ratiofiles[Element],'a')
        for x in range(maps_list[Element][0][0].shape[0]):
            for y in range(maps_list[Element][0][0].shape[1]):
                a = int(maps_list[Element][0][0][x][y])
                b = int(maps_list[Element][0][1][x][y])
                if b > 0: 
                    r_file.write("{}\t{}\t{}\t{}\t{}\n".format(x,y,a,b,a/b))
                    logging.debug("{}\t{}\t{}\t{}\t{}\n".format(x,y,a,b,a/b))
                else: 
                    r_file.write("{}\t{}\t{}\t{}\t{}\n".format(x,y,a,b,0))
                    logging.debug("{}\t{}\t{}\t{}\t{}\n".format(x,y,a,b,0))
        r_file.close()
    return 0

def linregress(x, y, sigmay=None, full_output=False):

    # DISCLAIMER #
    # function extracted from PyMca5.PyMcaMath.fitting.RateLaw script

    """
    Linear fit to a straight line following P.R. Bevington:
    
    "Data Reduction and Error Analysis for the Physical Sciences"

    Parameters
    ----------
    x, y : array_like
        two sets of measurements.  Both arrays should have the same length.

    sigmay : The uncertainty on the y values
        
    Returns
    -------
    slope : float
        slope of the regression line
    intercept : float
        intercept of the regression line
    r_value : float
        correlation coefficient

    if full_output is true, an additional dictionary is returned with the keys

    sigma_slope: uncertainty on the slope

    sigma_intercept: uncertainty on the intercept

    stderr: float
        square root of the variance
    
    """

    x = np.asarray(x, dtype=np.float).flatten()
    y = np.asarray(y, dtype=np.float).flatten()
    N = y.size
    if sigmay is None:
        sigmay = np.ones((N,), dtype=y.dtype)
    else:
        sigmay = np.asarray(sigmay, dtype=np.float).flatten()
    w = 1.0 / (sigmay * sigmay + (sigmay == 0))

    n = S = w.sum()
    Sx = (w * x).sum()
    Sy = (w * y).sum()    
    Sxx = (w * x * x).sum()
    Sxy = ((w * x * y)).sum()
    Syy = ((w * y * y)).sum()
    # SSxx is identical to delta in Bevington book
    delta = SSxx = (S * Sxx - Sx * Sx)

    tmpValue = Sxx * Sy - Sx * Sxy
    intercept = tmpValue / delta
    SSxy = (S * Sxy - Sx * Sy)
    slope = SSxy / delta
    sigma_slope = np.sqrt(S /delta)
    sigma_intercept = np.sqrt(Sxx / delta)

    SSyy = (n * Syy - Sy * Sy)
    r_value = SSxy / np.sqrt(SSxx * SSyy)
    if r_value > 1.0:
        r_value = 1.0
    if r_value < -1.0:
        r_value = -1.0

    if not full_output:
        return slope, intercept, r_value

    ddict = {}
    # calculate the variance
    if N < 3:
        variance = 0.0
    else:
        variance = ((y - intercept - slope * x) ** 2).sum() / (N - 2)
    ddict["variance"] = variance
    ddict["stderr"] = np.sqrt(variance)
    ddict["slope"] = slope
    ddict["intercept"] = intercept
    ddict["r_value"] = r_value
    ddict["sigma_intercept"] = np.sqrt(Sxx / SSxx)
    ddict["sigma_slope"] = np.sqrt(S / SSxx)
    return slope, intercept, r_value, ddict

if __name__ == "__main__":
    logging.info("This is SpecRead")
