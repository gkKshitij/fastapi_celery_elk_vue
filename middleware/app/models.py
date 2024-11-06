from sqlmodel import SQLModel, Field, Column, Integer, String, ARRAY#, create_engine, Relationship
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from app.db import Base


class Audit(Base):
    __tablename__ = "audit"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    headers = Column("headers", ARRAY(String))
    method = Column(String)
    response = Column(String)


class SongBase(SQLModel):
    name: str
    artist: str
    year: Optional[int] = None


class Song(SongBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)


class SongCreate(SongBase):
    pass


class Item(BaseModel):
    name: str

######################################################################
class OneDriveFile(SQLModel, table=True):
    RecordID: Optional[int] = Field(default=None, primary_key=True)
    fileHash: str = Field(nullable=False, unique=True)
    fileName: str
    filePath: str
    fileType: str
    createdDate: datetime = Field(default_factory=datetime.utcnow)
    modifiedDate: datetime = Field(default_factory=datetime.utcnow)
    owner: str

class SystemFile(SQLModel, table=True):
    RecordID: Optional[int] = Field(default=None, primary_key=True)
    fileHash: str = Field(nullable=False, unique=True)
    fileName: str
    filePath: str
    fileType: str
    createdDate: datetime = Field(default_factory=datetime.utcnow)
    modifiedDate: datetime = Field(default_factory=datetime.utcnow)
    owner: str
    peripherialID: str # = Field(foreign_key='peripheralmachines.macidHash')

class PeripheralMachines(SQLModel, table=True):
    RecordID: Optional[int] = Field(default=None, primary_key=True)
    macidHash: str = Field(nullable=False, unique=True)
    isActive: bool = Field(default=True)
    isAvailable: bool = Field(default=True)
    lastActive: datetime = Field(default_factory=datetime.utcnow)

class DatabaseScan(SQLModel, table=True):
    RecordID: Optional[int] = Field(default=None, primary_key=True)
    scanHash: str = Field(nullable=False, unique=True)
    authenticationMethod: str
    username: str
    serverAddress: str
    databaseName: str
    databaseType: str
    tableName: str
    columnName: str
    columnType: str

class ScanResult(SQLModel, table=True):
    scanId: Optional[int] = Field(default=None, primary_key=True)
    scanTypeID: int #= Field(foreign_key='scantypenotation.scanTypeID')
    scanStatusID: int #= Field(foreign_key='scanstatusnotation.scanStatusID')
    scanSessionID: str #= Field(foreign_key='session.sessionId')
    scannedByID: int #= Field(foreign_key='user.userId')
    scanDate: datetime #= Field(default_factory=datetime.utcnow)
    TotalPII_entries: int
    SeverityCritical: int
    SeverityHigh: int
    SeverityLow: int
    ReportLink: str

    # onedrivefile: Optional["OneDriveFile"] = Relationship(back_populates="scanresults")
    # systemfile: Optional["SystemFile"] = Relationship(back_populates="scanresults")
    # databasescan: Optional["DatabaseScan"] = Relationship(back_populates="scanresults")
    # scantypenotation: Optional["ScanTypeNotation"] = Relationship(back_populates="scanresults")
    # scanstatusnotation: Optional["ScanStatusNotation"] = Relationship(back_populates="scanresults")
    # user: Optional["User"] = Relationship(back_populates="scanresults")

class ScanTypeNotation(SQLModel, table=True):
    scanTypeID: Optional[int] = Field(default=None, primary_key=True)
    scanType: str

class ScanStatusNotation(SQLModel, table=True):
    scanStatusID: Optional[int] = Field(default=None, primary_key=True)
    scanStatus: str

class User(SQLModel, table=True):
    userId: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(nullable=False, unique=True)
    pwdh: str
    email: str
    company: str

class License(SQLModel, table=True):
    licenseId: Optional[int] = Field(default=None, primary_key=True)
    licenseKey: str = Field(nullable=False, unique=True)
    startDate: datetime = Field(default_factory=datetime.utcnow)
    expiryDate: datetime
    company: str

class UserLicense(SQLModel, table=True):
    userLicenseID: Optional[int] = Field(default=None, primary_key=True)
    userId: int # = Field(foreign_key='user.userId')
    licenseId: int # = Field(foreign_key='license.licenseId')
    assignedDate: datetime = Field(default_factory=datetime.utcnow)
    status: bool = Field(default=True)

class Session(SQLModel, table=True):
    sessionId: Optional[str] = Field(default=None, primary_key=True)
    userId: int # = Field(foreign_key='user.userId')
    loginTime: datetime = Field(default_factory=datetime.utcnow)
    lastActiveTime: datetime = Field(default_factory=datetime.utcnow)
    ipAddress: str

