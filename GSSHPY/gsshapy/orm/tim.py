'''
********************************************************************************
* Name: TimeSeriesModel
* Author: Nathan Swain
* Created On: Mar 18, 2013
* Copyright: (c) Brigham Young University 2013
* License: BSD 2-Clause
********************************************************************************
'''

__all__ = ['TimeSeriesFile',
           'TimeSeries',
           'TimeSeriesValue']

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Integer, Float, String
from sqlalchemy.orm import relationship

from gsshapy.orm import DeclarativeBase
from gsshapy.orm.file_base import GsshaPyFileObjectBase

from gsshapy.lib.pivot import pivot

class TimeSeriesFile(DeclarativeBase, GsshaPyFileObjectBase):
    '''
    classdocs
    '''
    
    __tablename__ = 'tim_time_series_files'
    
    # Primary and Foreign Keys
    id = Column(Integer, autoincrement=True, primary_key=True)
    projectFileID = Column(Integer, ForeignKey('prj_project_files.id'))
    
    # Value Columns
    fileExtension = Column(String, nullable=False)
    
    # Relationship Properties
    projectFile = relationship('ProjectFile', back_populates='timeSeriesFiles')
    timeSeries = relationship('TimeSeries', back_populates='timeSeriesFile')
    
    def __init__(self, directory, filename, session):
        '''
        Constructor
        '''
        GsshaPyFileObjectBase.__init__(self, directory, filename, session)
        
    def read(self):
        '''
        Generic Time Series Read from File Method
        '''
        # Assign file extension attribute to file object
        self.fileExtension = self.EXTENSION
        
        timeSeries = []
        
        # Open file and parse into a data structure
        with open(self.PATH, 'r') as f:
            for line in f:
                sline = line.strip().split()
                
                record = {'time': sline[0],
                          'values': []}
                
                for idx in range(1, len(sline)):
                    record['values'].append(sline[idx])
                
                timeSeries.append(record)
        
        self._createTimeSeriesObjects(timeSeries)
        
        
    def write(self, directory, session, filename):
        '''
        Generic Time Series Write to File Method
        '''
        # Initiate file
        fullPath = '%s%s' % (directory, filename)
        
        # Retrieve all time series
        timeSeries = self.timeSeries
        
        # Num TimeSeries
        numTS = len(timeSeries)

        # Transform into list of dictionaries for pivot tool
        valList = []
        
        for tsNum, ts in enumerate(timeSeries):
            values = ts.values
            for value in values:
                valDict = {'time': value.simTime,
                           'tsNum': tsNum,
                           'value': value.value}
                valList.append(valDict)
        
        # Use pivot function (from lib) to pivot the values into 
        # a format that is easy to write.
        result = pivot(valList, ('time',), ('tsNum',), 'value')
        
        # Open file and write
        with open(fullPath, 'w') as tsFile:
            for line in result:
                
                valString = ''
                # Compile value string
                for n in range(0, numTS):
                    val = '%.6f' % line[(n,)]
                    valString = '%s%s%s' % (
                                 valString,
                                 ' '*(13-len(str(val))), # Fance spacing trick
                                 val)
                    
                tsFile.write('   %.8f%s\n' % (line['time'], valString))
            
        
    def _createTimeSeriesObjects(self, timeSeries):
        '''
        Create GSSHAPY TimeSeries and TimeSeriesValue Objects Method
        '''
        
        # Determine number of value columns
        valColumns = len(timeSeries[0]['values'])
        
        # Create List of GSSHAPY TimeSeries objects
        series = []
        for i in range(0, valColumns):
            ts = TimeSeries()
            ts.timeSeriesFile = self
            series.append(ts)
        
        for record in timeSeries:
            for index, value in enumerate(record['values']):
                # Create GSSHAPY TimeSeriesValue objects
                tsVal = TimeSeriesValue(simTime=record['time'],
                                        value=value)
                
                # Associate with appropriate TimeSeries object via the index
                tsVal.timeSeries = series[index]
         
        
class TimeSeries(DeclarativeBase):
    '''
    classdocs
    '''
    
    __tablename__ = 'tim_time_series'
    
    # Primary and Foreign Keys
    id = Column(Integer, autoincrement=True, primary_key=True)
    timeSeriesFileID = Column(Integer, ForeignKey('tim_time_series_files.id'))
    
    # Relationship Properties
    timeSeriesFile = relationship('TimeSeriesFile', back_populates='timeSeries')
    values = relationship('TimeSeriesValue', back_populates='timeSeries') 



class TimeSeriesValue(DeclarativeBase):
    '''
    classdocs
    '''
    
    __tablename__ = 'tim_time_series_values'
    
    # Primary and Foreign Keys
    id = Column(Integer, autoincrement=True, primary_key=True)
    timeSeriesID = Column(Integer, ForeignKey('tim_time_series.id'), nullable=False)
    
    # Value Columns
    simTime = Column(Float, nullable=False)
    value = Column(Float, nullable=False)
    
    # Relationship Properties
    timeSeries = relationship('TimeSeries', back_populates='values')
    
    def __init__(self, simTime, value):
        '''
        Constructor
        '''
        self.simTime = simTime
        self.value = value
        
    def __repr__(self):
        return '<TimeSeriesValue: Time=%s, Value=%s>' % (self.simTime, self.value)