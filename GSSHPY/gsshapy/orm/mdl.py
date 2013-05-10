'''
********************************************************************************
* Name: ModelInstanceModel
* Author: Nathan Swain
* Created On: Mar 18, 2013
* Copyright: (c) Brigham Young University 2013
* License: BSD 2-Clause
********************************************************************************
'''

__all__ = ['ModelInstance']

from sqlalchemy import Column
from sqlalchemy.types import Integer, DateTime, String
from sqlalchemy.orm import relationship

from model.gsshapy import DeclarativeBase


class ModelInstance(DeclarativeBase):
    """
    classdocs

    """
    __tablename__ = 'model_instances'
    
    # Primary and Foreign Keys
    id = Column(Integer, autoincrement=True, primary_key=True)
    
    # Value Columns
    name = Column(String, nullable=False)
    location = Column(String)
    beginDate = Column(DateTime)
    endDate = Column(DateTime)
    
    # Relationship Properties
    projectOptions = relationship('ProjectOption', back_populates='model')
    mapTable = relationship('MapTable', back_populates='model')
    timeseries = relationship('TimeSeries', back_populates='model')
    
    def __init__(self, name, location='', beginDate=None, endDate=None):
        '''
        Constructor
        '''
        self.name = name
        self.location = location
        self.beginDate = beginDate
        self.endDate = endDate
        

    def __repr__(self):
        return '<ModelInstance: Name=%s, Location=%s, StartDate=%s, EndDate=%s>' % (self.name, self.location, self.beginDate, self.endDate)