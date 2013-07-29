'''
********************************************************************************
* Name: Input File Readers
* Author: Nathan Swain
* Created On: July 29, 2013
* Copyright: (c) Brigham Young University 2013
* License: BSD 2-Clause
********************************************************************************
'''
from gsshapy.orm.cmt import MapTableFile
from gsshapy.orm.gag import PrecipFile
from gsshapy.orm.cif import ChannelInputFile
from gsshapy.orm.spn import StormPipeNetworkFile
from gsshapy.orm.hmet import HmetFile

def readMappingTableFile(projectFile, filename):
    '''
    Initiate Read Mapping Table File Method
    '''
    # Initiate GSSHAPY MapTableFile object, associate with this object, and read map table file
    mapTable = MapTableFile(directory=projectFile.DIRECTORY, filename=filename, session=projectFile.SESSION)
    mapTable.projectFile = projectFile
    mapTable.read()
    print 'Mapping Table File Read'

def readPrecipitationFile(projectFile, filename):
    '''
    Initiate Read Precipitation File Method
    '''
    # Initiate GSSHAPY PrecipFile object, associate it with this object, and read precipitation file
    precip = PrecipFile(directory=projectFile.DIRECTORY, filename=filename, session=projectFile.SESSION)
    precip.projectFile = projectFile
    precip.read()
    print 'Precipitation File Read'
    
def readPipeNetworkFile(projectFile, filename):
    '''
    Initiate Read Storm Pipe Network File Method
    '''
    # Initiate GSSHAPY StormPipeNetworkFile object, associate with this object, and read file
    pipeNetworkFile = StormPipeNetworkFile(directory=projectFile.DIRECTORY, filename=filename, session=projectFile.SESSION)
    pipeNetworkFile.projectFile = projectFile
    pipeNetworkFile.read()
    print 'Pipe Network File Read'
    
def readChannelInputFile(projectFile, filename):
    '''
    Initiate Read Channel Input File Method
    '''
    # Initiate GSSHAPY ChannelNetworkFile object, associate with this object, and read channel input file
    channelInputFile = ChannelInputFile(directory=projectFile.DIRECTORY, filename=filename, session=projectFile.SESSION)
    channelInputFile.projectFile = projectFile
    channelInputFile.read()
    print 'Channel Input File Read'
    
def readHmetWesFile(projectFile, filename):
    '''
    Initiate Read HMET_WES File Method
    '''
    hmet = HmetFile(directory=projectFile.DIRECTORY, filename=filename, session=projectFile.SESSION)
    hmet.projectFile = projectFile
    hmet.readWES()
    print 'HMET_WES File Read'