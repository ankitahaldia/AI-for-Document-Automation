import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound


from packages.DAL import database_objects as dbo
from packages.serv.services import to_date


#boiler code ORM SqlAlchemy
engine = create_engine('sqlite:///testdb.db', echo=True)
Base = dbo.Base
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
   

#GET
def get_themes(themes_series, session):
    '''
    gets themes based on a series of french theme names.
    '''
    themes = []

    if themes_series[0] is not None: 
        themes = session.query(dbo.Theme).filter(dbo.Theme.name_fr.in_(themes_series[0])).all()

    return themes

def get_all_themes():

    session = Session()
    themes = session.query(dbo.Theme).all()
    session.close()

    return themes

def get_cla_by_theme(theme):
    session = Session()
    try :
        db_theme = session.query(dbo.Theme).filter(dbo.Theme.name_fr == theme).first()
        return db_theme.CLAs
    
    except NoResultFound:
        return []

def get_cla_full_search(theme, jc_id, is_errated, start_sig_date, end_sig_date):
    clas = get_cla_by_theme(theme)
    clas = [cla for cla in clas if 
        cla.joint_commission_id == jc_id 
        and (not is_errated or cla.corrected_date is not None )
        and cla.signature_date > start_sig_date
        and cla.signature_date < end_sig_date]

    return clas

def get_all_jc():

    session = Session()
    jcs = session.query(dbo.JointCommission).all()
    session.close()

    return jcs



#INSERT 
def insert_scope(df):
    db_scopes = []
    session = Session()

    df1 = df.dropna(subset=['scopeNl'])

    for _, row in df1.iterrows():    
        length = len(row['scopeNl'])
        for j in range(length):
            db_scopes.append(dbo.Scope(name_fr=row['scopeFr'][j], name_nl=row['scopeNl'][j], CLA_id=row['depositNumber']))
    
    session.bulk_save_objects(db_scopes)
    session.commit()

def insert_no_scope(df):
    db_no_scopes = []
    session = Session()

    df1 = df.dropna(subset=['noScopeNl'])

    for _, row in df1.iterrows():    
        length = len(row['noScopeNl'])
        for j in range(length):
            db_no_scopes.append(dbo.NoScope(name_fr=row['noScopeFr'][j], name_nl=row['noScopeNl'][j], CLA_id=row['depositNumber']))
    
    session.bulk_save_objects(db_no_scopes)
    session.commit()

def insert_joint_commission(df):
    session = Session()

    joint_coms = df.groupby(['jcId'])['jcId', 'jcFr', 'jcNl'].agg(lambda x: x.unique())

    db_jcs = [dbo.JointCommission(id=row['jcId'], name_fr=row['jcFr'], name_nl=row['jcNl']) for i,row in joint_coms.iterrows()]

    session.bulk_save_objects(db_jcs)
    session.commit()

def insert_themes(df):
    session = Session()

    list_fr = [themes for i,row in df.iterrows() if row['themesNl'] is not None for themes in row['themesFr']]
    list_nl = [themes for i,row in df.iterrows() if row['themesNl'] is not None for themes in row['themesNl']]
    themes = pd.DataFrame(list(zip(list_fr, list_nl)),columns =['themesFr', 'themesNl']).groupby('themesFr')['themesFr', 'themesNl'].agg(lambda x : x.unique())
    db_themes = [dbo.Theme(name_nl=row['themesNl'], name_fr=row['themesFr']) for i, row in themes.iterrows()]

    session.bulk_save_objects(db_themes)
    session.commit()

def insert_CLA(df):
    session = Session()

    db_CLAs = [dbo.CLA(
        id =row['depositNumber'],
        anenexe_page = 0,    
        title_fr = row['titleFr'],
        title_nl = row['titleNl'],
        signature_date = to_date(row['signatureDate']),
        validity_date = to_date(row['validityDate']),
        deposit_date = to_date(row['depositDate']),
        record_date = to_date(row['recordDate']),
        deposit_registration_date = to_date(row['depositRegistrationDate']),
        royal_decree_date = to_date(row['royalDecreeDate']),
        notice_deposit_MB_date = to_date(row['noticeDepositMBDate']),
        publication_royal_decree_date = to_date(row['publicationRoyalDecreeDate']),
        corrected_date = to_date(row['correctedDate']),
        document_link = row['documentLink'],
        joint_commission_id = row['jcId'],
        themes = get_themes(row[['themesFr', 'themesNl']], session)) for i, row in df.iterrows()]

    for cla in db_CLAs:
        session.add(cla)
    session.commit()

#MISC
def check_for_new_cla(df):
    session = Session()
    new_clas = []
    errated_clas = []

    for _, row in df.iterrows():
        print(row['depositNumber'])
        try :
            cla = session.query(dbo.CLA).filter(dbo.CLA.id == row['depositNumber']).one()
            
            if row['correctedDate'] is not None and cla.corrected_date != to_date(row['correctedDate']):
                errated_clas.append(row)
        
        except NoResultFound :
            new_clas.append(row)
    session.close()    
    return new_clas, errated_clas

