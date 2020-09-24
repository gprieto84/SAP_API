from sqlalchemy import Column, Integer, String, DateTime, Numeric, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from config import Base


notification_columns = {'QMNUM':'n_number', 'IWERK':'plant','QMART':'type_n','AUFNR':'order','EQUNR':'equipment','QMTXT':'description', \
    'STRMN':'required_start_date','LTRMN':'required_end_date','ERDAT':'creation_date','PRIOK':'priority','ERNAM':'created_by', \
    'TPLNR':'func_location', 'ARBPL':'work_center', 'OBJNR':'obj_nr' }

class Notification(Base): #VIQMEL
    __tablename__ = 'SAP_notifications'

    n_number = Column(String(20), primary_key=True) #QMNUM
    plant =  Column(String) #IWERK
    type_n = Column(String, nullable= False) #QMART
    order = Column(String) #AUFNR
    equipment = Column(String, nullable= False) #EQUNR
    description = Column(String) #QMTXT
    required_start_date = Column(DateTime) #STRMN
    required_end_date = Column(DateTime) #LTRMN
    creation_date = Column(DateTime, nullable=False) #ERDAT
    priority = Column(String) #PRIOK
    created_by = Column(String, nullable = False) #ERNAM
    func_location = Column(String) #TPLNR
    work_center = Column(Integer) #ARBPL
    obj_nr = Column(String,nullable = False) #OBJNR

notification_type_columns = {'QMART':'type_n', 'STSMA':'status_schema'}
class Notification_Type(Base): #TQ80
    __tablename__ = 'SAP_notification_type'
    
    type_n = Column(String(20), primary_key=True) #QMART
    status_schema = Column(String(20)) #STSMA

notification_text_columns = {'QMNUM':'n_number', 'FETXT':'short_text'}
class Notification_Text(Base): #QMFE
    __tablename__ = 'SAP_notification_text'
    
    id = Column(Integer, primary_key=True, autoincrement=True) #ID
    n_number = Column(String(20), nullable= False) #QMNUM
    short_text = Column(String) #FETXT

notification_activity_columns = {'QMNUM':'n_number', 'MATXT':'activity_text','MNGRP':'group','MNCOD':'code', 'MNKAT':'catalog'}
class Notification_Activity(Base): #QMMA
    __tablename__ = 'SAP_notification_activities'
    
    id = Column(Integer, primary_key=True, autoincrement=True) #ID
    n_number = Column(String(20), nullable= False) #QMNUM
    group = Column(String(30), nullable= False) #MNGRP
    code = Column(String(20)) #MNCOD
    activity_text = Column(String) #MATXT
    catalog = Column(String) #MNKAT

notification_activity_header_columns = {'CODEGRUPPE':'group', 'CODE':'code', 'KURZTEXT':'description', 'KATALOGART':'catalog'}
class Notification_Activity_Header(Base): #QPCT
    __tablename__ = 'SAP_notification_activities_header'
    
    id = Column(Integer, primary_key=True, autoincrement=True) #ID
    group = Column(String(30), nullable= False) #CODEGRUPPE
    code = Column(String(20)) #CODE
    description = Column(String) #KURZTEXT
    catalog = Column(String) #KATALOGART

notification_catalog_columns = {'KATALOGART':'catalog', 'KATALOGTXT':'description'}
class Notification_Catalog(Base): #TQ15T
    __tablename__ = 'SAP_notification_catalog'
    
    catalog = Column(String(10),primary_key=True ) #KATALOGART
    description = Column(String(100), nullable= False) #KATALOGTXT


notification_cause_columns = {'QMNUM':'n_number', 'URTXT':'cause'}
class Notification_Cause(Base): #QMUR
    __tablename__ = 'SAP_notification_causes'
    
    id = Column(Integer, primary_key=True, autoincrement=True) #ID
    n_number = Column(String(20), nullable= False) #QMNUM
    cause = Column(String) #URTXT

equipment_columns = {'EQUNR':'equipment', 'EQART':'type_e','HERST':'manufacturer', 'TYPBZ':'model'}
class Equipment(Base): #EQUI
    __tablename__ = 'SAP_equipments'

    equipment = Column(String(20), primary_key=True) #EQUNR
    type_e = Column(String, nullable= False) #EQART
    manufacturer = Column(String) #HERST
    model = Column(String) #TYPBZ

equipment_text_columns = {'EQUNR':'equipment', 'EQKTX':'description'}
class Equipment_Text(Base):#EQKT
    __tablename__ = 'SAP_equipment_text'

    id = Column(Integer, primary_key=True,autoincrement=True)
    equipment = Column(String, nullable= False) #EQUNR
    description = Column(String, nullable= False) #EQKTX

work_center_columns = {'OBJID':'work_center', 'ARBPL':'description', 'KTEXT':'information'}
class Work_Center(Base): #CRHD
    __tablename__ = 'SAP_work_center'

    work_center = Column(String(20), primary_key=True) #OBJID
    description = Column(String) #ARBPL
    information = Column(String) #KTEXT

func_location_columns =  {'TPLNR':'func_location', 'STRNO':'description', 'ACTVS':'active','TPLKZ':'indicator','ERDAT':'creation_date',\
    'VERSN':'version', 'ERNAM':'created_by' }
class Functional_Location(Base): #IFLOS
    __tablename__ = 'SAP_functional_location'

    id = Column(Integer, primary_key=True,autoincrement=True)
    func_location = Column(String(50), primary_key=True) #TPLNR
    description = Column(String) #STRNO
    active = Column(String(5)) #ACTVS
    indicator = Column(String(20)) #TPLKZ
    creation_date = Column(String(20)) #ERDAT
    version = Column(String(5)) #VERSN
    created_by = Column(String(20)) #ERNAM
    

system_columns = {'ISTAT':'status_id', 'TXT04':'code','TXT30':'description'}
class System_Status(Base):#TJ02
    __tablename__ = 'SAP_system_status'

    status_id = Column(String(20), primary_key=True) #ISTAT
    code = Column(String(20),nullable = False) #TXT04
    description = Column(String,nullable = False) #TXT30

user_columns = {'STSMA':'status_schema','ESTAT':'status_id','TXT04':'code','TXT30':'description'}
class User_Status(Base):#TJ30T
    __tablename__ = 'SAP_user_status'

    id = Column(Integer, primary_key=True,autoincrement=True)
    status_schema = Column(String(20)) #STSMA
    status_id = Column(String,nullable = False) #ESTAT
    code = Column(String(20),nullable = False) #TXT04
    description = Column(String,nullable = False) #TXT30

status_columns = {'OBJNR':'obj_nr', 'STAT':'status_id','INACT':'disabled'}
system_status_columns = {'OBJNR':'obj_nr', 'STAT':'status_id','INACT':'disabled'}
class Notification_System_Status(Base):
    __tablename__ = 'SAP_notification_system_status'

    id = Column(Integer, primary_key=True,autoincrement=True)
    obj_nr = Column(String,nullable = False) #OBJNR
    status_id = Column(String,nullable = False) #STAT
    disabled = Column(String(3)) #INACT

user_status_columns = {'OBJNR':'obj_nr', 'STSMA':'status_schema','STAT':'status_id','INACT':'disabled'}
class Notification_User_Status(Base):
    __tablename__ = 'SAP_notification_user_status'

    id = Column(Integer, primary_key=True,autoincrement=True)
    obj_nr = Column(String,nullable = False) #OBJNR
    status_schema = Column(String(20)) #STSMA
    status_id = Column(String,nullable = False) #STAT
    disabled = Column(String(3)) #INACT

log_columns = {'OBJNR':'obj_nr', 'STAT':'status_id','USNAM':'changed_by','UDATE':'change_date','UTIME':'changed_time','INACT':'inactive','CHIND':'change_indicator'}
class Notification_Log_System(Base):
    __tablename__ = 'SAP_status_log_system'

    id = Column(Integer, primary_key=True, autoincrement=True)
    obj_nr = Column(String,nullable = False) #OBJNR
    status_id = Column(String,nullable = False) #STAT
    changed_by = Column(String,nullable = False) #USNAM
    change_date = Column(String,nullable = False) #UDATE
    changed_time = Column(String,nullable = False) #UTIME
    inactive = Column(String) #INACT
    change_indicator = Column(String) #CHIND

class Notification_Log_User(Base):
    __tablename__ = 'SAP_status_log_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    obj_nr = Column(String,nullable = False) #OBJNR
    status_id = Column(String,nullable = False) #STAT
    changed_by = Column(String,nullable = False) #USNAM
    change_date = Column(String,nullable = False) #UDATE
    changed_time = Column(String,nullable = False) #UTIME
    inactive = Column(String) #INACT
    change_indicator = Column(String) #CHIND
    status_schema = Column(String(20)) #STSMA









    





