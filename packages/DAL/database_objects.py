from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import backref, relationship
from sqlalchemy import Column, Integer, String, Date, Table

Base = declarative_base()

# Jointure tables
theme_CLA = Table('Theme_CLA', Base.metadata,
    Column('CLA_id', Integer, ForeignKey('CLAs.id')),
    Column('name_fr', Integer, ForeignKey('Themes.name_fr')))
 

# Normal tables
class JointCommission(Base):
    __tablename__ = 'Joint_commissions'

    id = Column(Integer, primary_key=True)
    name_fr = Column(String, unique=True)
    name_nl = Column(String, unique=True)    
    CLAs = relationship('CLA', back_populates='joint_commission')

class CLA(Base):
    __tablename__ = 'CLAs'

    id = Column(Integer, primary_key=True)
    anenexe_page = Column(Integer)    
    title_fr = Column(String)
    title_nl = Column(String)
    signature_date = Column(Date, nullable=True)
    validity_date = Column(Date, nullable=True)
    deposit_date = Column(Date, nullable=True)
    record_date = Column(Date, nullable=True)
    deposit_registration_date = Column(Date, nullable=True)
    royal_decree_date = Column(Date, nullable=True)
    notice_deposit_MB_date = Column(Date, nullable=True)
    publication_royal_decree_date = Column(Date, nullable=True)
    corrected_date = Column(Date, nullable=True)
    document_link = Column(String)
    joint_commission_id = Column(Integer, ForeignKey('Joint_commissions.id'))
    joint_commission = relationship('JointCommission', back_populates='CLAs')
    

    # these are other relationships, they are not relevant for our demonstration
    errata = relationship('Erratum', back_populates='CLA')
    themes = relationship('Theme', secondary=theme_CLA, lazy='subquery', backref=backref('Themes', lazy=True))
    scopes = relationship('Scope', back_populates='CLA')
    no_scopes = relationship('NoScope', back_populates='CLA')


    def __str__(self):
        link = r'https://public-search.emploi.belgique.be/website-download-service/joint-work-convention/'
        
        if self.themes:
            themes = '\n'.join([th.name_fr for th in self.themes])
        else : 
            themes = []
        if self.scopes:
            scopes = ['\n'.join(i.name_fr) for i in self.scopes]
        else :
            scopes = []
        if self.no_scopes:
            no_scopes = ['\n'.join(i.name_fr) for i in self.no_scopes]
        else :
            no_scopes = []
        return (f'''
        SECTOR:
        \n
        {self.joint_commission.name_fr}
        \n
        {self.title_fr}\n
        \n
        has been errated: {self.corrected_date is not None}
        \n
        THEMES: 
        \n
        {themes}
        \n
        SCOPES: 
        \n
        {scopes}
        \n
        NO SCOPES: 
        \n
        {no_scopes}
        \n
        signature date: {self.signature_date} 
        \n
        validity date: {self.validity_date}
        \n
        deposit date: {self.deposit_date}
        \n
        record date: {self.record_date}
        \n
        download link : {link}{self.document_link}
        ''')


class Erratum(Base):
    __tablename__ = 'Errata'

    id = Column(Integer, primary_key=True)
    CLA_id = Column(Integer, ForeignKey('CLAs.id'))
    CLA = relationship('CLA', back_populates='errata')
    #TODO : paragraphID FK
    
class Theme(Base):
    __tablename__ = 'Themes'
    
    name_fr = Column(String, primary_key=True)
    name_nl = Column(String)
    CLAs = relationship('CLA', secondary=theme_CLA, lazy='subquery',  backref=backref('CLAs', lazy=True))

class Scope(Base):
    __tablename__ = 'Scopes'

    id = Column(Integer, primary_key=True)
    name_fr = Column(String)
    name_nl = Column(String)
    CLA_id = Column(Integer, ForeignKey('CLAs.id'))
    CLA = relationship('CLA', back_populates='scopes')
    
class NoScope(Base):
    __tablename__ = 'No_scopes'

    id = Column(Integer, primary_key=True)
    name_fr = Column(String)
    name_nl = Column(String)
    CLA_id = Column(Integer, ForeignKey('CLAs.id'))
    CLA = relationship('CLA', back_populates='no_scopes')
