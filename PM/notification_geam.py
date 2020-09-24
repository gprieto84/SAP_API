from config import Session, engine, Base, sap_conn
import datetime
import pandas as pd
from PM.models import Notification, notification_columns, Notification_Text, notification_text_columns, Notification_Activity, notification_activity_columns,\
    Notification_Cause, notification_cause_columns, Equipment, equipment_columns, Equipment_Text, equipment_text_columns, Work_Center, work_center_columns,\
    Functional_Location, func_location_columns,Notification_System_Status, system_status_columns, Notification_Log_System, Notification_Log_User, log_columns, notification_activity_header_columns, Notification_Activity_Header, \
    notification_type_columns, Notification_Type, user_status_columns, Notification_User_Status, system_columns, System_Status, user_columns, User_Status, status_columns, notification_catalog_columns,\
    Notification_Catalog
import os

def clean_list(sap_list, split_value):
    return_list = []
    for value in sap_list:
        clean_value = [i.strip(' ') for i in value['WA'].split(split_value)]
        return_list.append(clean_value)
    return return_list

def SAP_process_table(table, fields, options, columns_dict, model):
    session = Session()
    df = SAP_get_table(table, fields,options )
    df.rename(columns=columns_dict,inplace=True)
    session.execute(model.__table__.insert(),df.to_dict(orient="records"))
    session.commit()
    session.close()
    return df

def SAP_get_table(table, fields, options, rows=1000000, delimeter='ɷ'):
    result = sap_conn.call('RFC_READ_TABLE', \
        QUERY_TABLE = table, \
        FIELDS = fields, \
        OPTIONS = [{ 'TEXT': options}], \
        ROWCOUNT = rows, DELIMITER=delimeter)
        
    cleaned_list = clean_list(result["DATA"], delimeter)
    return pd.DataFrame(cleaned_list, columns=fields)

def SAP_get_table_by_data(table, fields, options, data):
    i = 0
    df_ret = pd.DataFrame(columns=fields)
    for row in data:
        where = options.replace('#field#', row)
        if i % 500 == 0:
            print(i)
        df_ret = df_ret.append(SAP_get_table(table, fields, where ))
        i += 1
    return df_ret

def SAP_notification_process(date, end_date):
    # Get all notifications from the VIQMEL
    print('Processing notifications')
    #df_notification = SAP_process_table('VIQMEL',['QMNUM','IWERK','QMART','AUFNR','EQUNR','QMTXT','STRMN','LTRMN','ERDAT','PRIOK','ERNAM','TPLNR','ARBPL', 'OBJNR'],\
    #    "IWERK EQ 'TR01' AND ERDAT >= '" + date + "' and ERDAT <= '"+end_date+"'",notification_columns, Notification)
    df_notification = pd.read_sql_table("SAP_notifications",con=engine)

    # Get all notifications´ types TQ80
    print('Processing notifications type')
    #SAP_process_table('TQ80', ['QMART','STSMA'], "MANDT EQ '020'",notification_type_columns, Notification_Type)
    df_type = pd.read_sql_table("SAP_notification_type",con=engine)

    # Get all notifications´ additional texts or comments QMFE
    print('Processing notifications text')
    #SAP_process_table('QMFE', ['QMNUM','FETXT'], "FETXT NE '' AND ERDAT >= '" + date + "'",notification_text_columns, Notification_Text)

    # Get all notifications' activities from the QMMA
    print('Processing notifications activities')
    #SAP_process_table('QMMA', ['MANDT','QMNUM','MATXT','MNGRP','MNCOD','MNKAT'], "MANDT EQ '020' AND ERDAT >= '" + date + "'", notification_activity_columns, Notification_Activity)

    # Get all notification´s activities header for the QPCD
    print('Processing notifications activities header')
    #SAP_process_table('QPCT', ['MANDT','CODEGRUPPE','CODE','KURZTEXT','KATALOGART'], "MANDT EQ '020' AND INAKTIV EQ ''", notification_activity_header_columns, Notification_Activity_Header)

    # Get all notification´s catalog types for the TQ15
    print('Processing notifications catalog')
    #SAP_process_table('TQ15T', ['MANDT','KATALOGART','KATALOGTXT'], "MANDT EQ '020' AND SPRACHE EQ 'S'", notification_catalog_columns, Notification_Catalog)

    # Get all notifications' causes from the QMUR
    print('Processing notifications causes')
    #SAP_process_table('QMUR', ['MANDT','QMNUM','URTXT'], "MANDT EQ '020' AND ERDAT >= '" + date + "'", notification_cause_columns, Notification_Cause)
    
    # Get all TRANSELCA´s equipment (K: Equipos Transelca - L: MAF Transelca)
    print('Processing equipments')
    #SAP_process_table('EQUI', ['MANDT','EQUNR','EQART','HERST','TYPBZ'], "EQTYP EQ 'K' OR EQTYP EQ 'L'", equipment_columns, Equipment)
    
    # Get all equipments´ descriptions
    print('Processing equipments description')
    #SAP_process_table('EQKT', ['MANDT','EQUNR','EQKTX'], "MANDT EQ '020'", equipment_text_columns, Equipment_Text)
    
    # Get all TRANSELCA's workplaces
    print('Processing workplaces')
    #df_workplace_id = SAP_get_table('CRHD',['MANDT','OBJID','ARBPL'],"MANDT EQ '020' AND WERKS EQ 'TR01'")
    #df_workplace_text = SAP_get_table('CRTX',['MANDT','OBJID','KTEXT'],"MANDT EQ '020' AND SPRAS EQ 'S'")
    #df_workplace = pd.merge(df_workplace_id, df_workplace_text, how='inner', on=['OBJID']) # filter per values in df_system
    #df_workplace.rename(columns=work_center_columns,inplace=True)
    #session = Session()
    #session.execute(Work_Center.__table__.insert(),df_workplace.to_dict(orient="records"))
    #session.commit()
    #session.close()
    
    # Get all TRANSELCA's functional location
    print('Processing functional location')
    #session = Session()
    #print(df_notification['func_location'].unique().shape)
    #df_func = SAP_get_table_by_data('IFLOS',['TPLNR','STRNO', 'ACTVS','TPLKZ','ERDAT','VERSN','ERNAM'],"ACTVS EQ 'X' AND TPLNR EQ '#field#'",df_notification['func_location'].unique())
    #df_func = df_func.drop_duplicates()
    #df_func.rename(columns=func_location_columns,inplace=True)
    #session.execute(Functional_Location.__table__.insert(),df_func.to_dict(orient="records"))
    #session.commit()
    #session.close()

    # Get System Status
    print('Processing System Status Header')
    #df_system = SAP_process_table('TJ02T', ['ISTAT','TXT04','TXT30'], "SPRAS EQ 'S'", system_columns, System_Status)
    df_system = pd.read_sql_table("SAP_system_status",con=engine)

    # Get User Status Header
    print('Processing User Status Header')
    #df_user = SAP_process_table('TJ30T', ['STSMA','ESTAT','TXT04','TXT30'], "MANDT EQ '020' AND SPRAS EQ 'S'", user_columns, User_Status)
    df_user = pd.read_sql_table("SAP_user_status",con=engine)

    
    # Get all statuses
    print(df_notification.shape)
    print('GET STATUSES START')
    #session = Session()
    #df_status = SAP_get_table_by_data('JEST',['MANDT','OBJNR','STAT','INACT'],"MANDT EQ '020' AND OBJNR EQ '#field#'",df_notification['obj_nr'])
    #df_status = df_status.drop_duplicates()
    #df_status.rename(columns=status_columns,inplace=True)
    #df_status_system = pd.merge(df_status, df_system, how='inner', on=['status_id']) # filter per values in df_system
    
    #df_status_user =  pd.merge(df_status, df_user['status_id'].drop_duplicates(), how='inner', on=['status_id']) # filter per values in df_user
    #df_notification_2 = pd.merge(df_notification, df_type, how='inner', on=['type_n']) # filter per values in df_user
    #df_status_user_x = pd.merge(df_status_user, df_notification_2[['obj_nr','status_schema']], how='inner', on=['obj_nr'])
    
    #session.execute(Notification_System_Status.__table__.insert(),df_status_system.to_dict(orient="records"))
    #session.execute(Notification_User_Status.__table__.insert(),df_status_user_x.to_dict(orient="records"))
    #session.commit()
    #session.close()

    # Get log statuses
    print('GET LOG STATUSES START')
    session = Session()
    df_status_system = pd.read_sql_table('SAP_notification_system_status',con=engine)
    df_status_user_x = pd.read_sql_table('SAP_notification_user_status',con=engine)
    df_log_status = SAP_get_table_by_data('JCDS',['MANDT','OBJNR','STAT','USNAM','UDATE','UTIME','TCODE','CDTCODE','INACT','CHIND'],"MANDT EQ '020' AND UDATE >='"+date+"' AND OBJNR EQ '#field#'",df_notification['obj_nr'])
    df_log_status = df_log_status.drop_duplicates()
    df_log_status.rename(columns=log_columns,inplace=True)
    df_log_status_system = pd.merge(df_log_status, df_status_system[['obj_nr','status_id']], how='inner', on=['obj_nr','status_id'])
    df_log_status_user = pd.merge(df_log_status, df_status_user_x[['obj_nr','status_id','status_schema']], how='inner', on=['obj_nr','status_id']) # filter
    
    session.execute(Notification_Log_User.__table__.insert(),df_log_status_user.to_dict(orient="records"))
    session.execute(Notification_Log_System.__table__.insert(),df_log_status_system.to_dict(orient="records"))
    session.commit()
    session.close()

def load():
    print('PROCESS START')
    # generate database schema
    #Base.metadata.create_all(engine)
    #SAP_notification_process('20150101','20201231')
    #print('PROCESS END')

    # print('Processing ANLA 1')
    # df_anla_1 = SAP_get_table('ANLA', ['ANLN1','ANLN2','ANLKL','GEGST','ANLAR','ERNAM','ERDAT','AENAM','AEDAT','XLOEV','XSPEB','FELEI','KTOGR','XOPVW','ANLTP',\
    # 'ZUJHR','ZUPER','ZUGDT','AKTIV','ABGDT','DEAKT','GPLAB','BSTDT','ORD41','ORD42','ORD43','ORD44','ANLUE','ZUAWA','ANEQK','ANEQS','LIFNR',\
    # 'LAND1','LIEFE','HERST','EIGKZ','AIBN1','AIBN2','AIBDT','URJHR','URWRT','ANTEI','PROJN','EAUFN','MEINS','MENGE','TYPBZ','IZWEK','INKEN'],"BUKRS EQ 'TRAN'" )
    
    # print('Processing ANLA 2')
    # df_anla_2 = SAP_get_table('ANLA', ['ANLN1','ANLN2','EHWNR','GRUVO','GREIN','GRBND','GRBLT','GRLFD','FLURK','FLURN','FIAMT',\
    # 'STADT','GRUND','FEINS','GRUFL','INVNR','VBUND','SPRAS','TXT50','TXA50','XLTXID','XVERID','XTCHID','XKALID','XHERID','XLEAID','LEAFI',\
    # 'LVDAT','LKDAT','LEABG','LEJAR','LEPER','LRYTH','LEGEB','LBASW','LKAUF','LMZIN','LZINS','LTZBW','LKUZA','LKUZI','LLAVB','LEANZ','LVTNR'],"BUKRS EQ 'TRAN'" )

    # print('Processing ANLA 3')
    # df_anla_3 = SAP_get_table('ANLA', ['ANLN1','ANLN2','IVDAT','INVZU','VMGLI','XVRMW','WRTMA','EHWRT','AUFLA','EHWZU','LETXT','XAKTIV','ANUPD','LBLNR','XV0DT'\
    # ,'XV0NM','XV1DT','XV1NM','XV2DT','XV2NM','XV3DT','XV3NM','XV4DT','XV4NM','XV5DT','XV5NM','XV6DT','XV6NM','AIMMO','OBJNR','LEART','LVORS','GDLGRP',\
    # 'POSNR','XERWRT','XAFABCH','XANLGR','MCOA1','XINVM','SERNR','UMWKZ','LRVDAT','ACT_CHANGE_PM','HAS_TDDP','LAST_REORG_DATE'],"BUKRS EQ 'TRAN'" )

    # print('First Merge')
    # df_anla_temp = pd.merge(df_anla_1, df_anla_2,how='inner', on=['ANLN1','ANLN2'])
    
    # print('Second Merge')
    # df_anla = pd.merge(df_anla_temp, df_anla_3,how='inner', on=['ANLN1','ANLN2'])

    # print(df_anla.shape)
    # print(df_anla.memory_usage(index=True).sum())

    # print('saving to excel')
    # df_anla.to_excel('anla_final.xlsx')

    #print('Processing V_EQUI')
    #df = SAP_get_table('V_EQUI', ['EQUNR','ANLNR','ACT_CHANGE_AA','DATBI','EQKTX','HERST','SERGE', 'HERLD','INVNR'],"KOKRS EQ 'TRAN' and EQUNR EQ '000000000002009529'" )
    #df.to_excel('v_equi.xlsx')


    # print('Processing ANLU 1')
    # df_anlu_1 = SAP_get_table('ANLU', ['ANLN1','ANLN2','ZZSERNR','ZZPOSNR','ZZUNDGENEFEC','ZZUSOINTERNO','ZZTPLNR','ZZIDPROAN','ZZNOMPROAN','ZZIDPROAC','ZZNOMPROAC','ZZDOCUMEN','ZZNOTARIA'],"BUKRS EQ 'TRAN'" )
    
    # print('Processing ANLU 2')
    # df_anlu_2 = SAP_get_table('ANLU', ['ANLN1','ANLN2','ZZDELEHAC','ZZCIUDESC','ZZDEPARTA','ZZCIUDAD','ZZVEREDA','ZZDIRECC','ZZDOCPAGO'],"BUKRS EQ 'TRAN'" )
    
    # df_anlu = pd.merge(df_anlu_1, df_anlu_2,how='inner', on=['ANLN1','ANLN2'])
    
    # df_anlu.to_csv('anlu_final.csv')

    # print('Processing ANLZ')
    # df_anlz = SAP_get_table('ANLZ', ['ANLN1','ANLN2','BDATU','ADATU','KOSTL','WERKS','GSBER','LSTAR','MSFAK','XSTIL','STORT','CAUFN','PLAN1','PLAN2','RAUMN',\
    #    'IAUFN','IPROJ','TPLKZ','TPLNR','ANUPD','TXJCD','IPSNR','KFZKZ','PERNR','KOSTLV','FISTL','GEBER','FKBER','GRANT_NBR','GEBER2','FKBER2','GRANT_NBR2',\
    #    'FISTL2','IMKEY','PS_PSP_PNR2','BUDGET_PD','BUDGET_PD2','SEGMENT','PRCTR'],"BUKRS EQ 'TRAN'" )

    # df_anlz.to_csv('anlz_final.csv')

    print('Processing IFLOS')
    df_func = SAP_get_table('IFLOS',['TPLNR','STRNO'],"ACTVS EQ 'X' AND PRKEY EQ 'X'")
    print('Completed IFLOS')

    print("Processing ANLA")
    df_anla = SAP_get_table('ANLA',['ANLN1','ANLKL','ANLN2','TXT50', 'LAND1','INVNR','DEAKT','HERST', 'ACT_CHANGE_PM'],"BUKRS EQ 'TRAN'")


    print("Processing ANLZ")
    df_anlz = SAP_get_table('ANLZ',['ANLN1','ANLN2','KOSTL', 'WERKS','STORT'],"BUKRS EQ 'TRAN'")
    
    print("Processing V_EQUI")
    df_equi = SAP_get_table('V_EQUI', ['EQUNR','ANLNR','ACT_CHANGE_AA','DATBI','EQKTX','HERST','HERLD','INVNR','KOSTL','SWERK','STORT',"TPLNR", "BEBER"],
        "KOKRS EQ 'TRAN' AND DATBI EQ '99991231'" )
    print("V_EQUI rows: {}".format(df_equi.shape[0]))
    
    print("Processing ANLA + ANLZ")
    df_asset = pd.merge(df_anla, df_anlz, how='inner', on=['ANLN1','ANLN2'])
    df_asset.rename(columns={"ANLN1": "A_acti","ANLKL":"A_clase","DEAKT":"A_Descapitalizacion", "TXT50": "A_objt","HERST":"A_fabr", \
        "LAND1":"A_pais", "INVNR":"A_invn", "KOSTL":"A_cost","WERKS":"A_cent","STORT":"A_dane"}, inplace=True)
    df_equi.rename(columns={"EQUNR":"E_equi","ANLNR": "E_acti", "EQKTX": "E_objt","HERST":"E_fabr","HERLD":"E_pais", "INVNR":"E_invn",\
        "KOSTL":"E_cost","SWERK":"E_cent","STORT":"E_dane","BEBER":"E_plant"}, inplace=True)

    print("Anla rows: {} - Anlz rows: {} - Merged rows: {}".format(df_anla.shape[0], df_anlz.shape[0], df_asset.shape[0]))
    print("Asset columns: {}".format(df_asset.columns))

    del df_anla['ANLN2']
    print("Processing Asset + Equi")
    df_asset_equi = pd.merge(df_asset, df_equi, left_on=['A_acti'], right_on=['E_acti'], how='outer')
    print("Total rows: {}".format(df_asset_equi.shape[0]))
    print("Total columns: {}".format(df_asset_equi.columns))

    print("Adding Technical Location")
    df_total = pd.merge(df_asset_equi,df_func, on=['TPLNR'], how="left")
    df_total.rename(columns={"STRNO":"ubi_tec"})
    print("Total rows: {}".format(df_total.shape[0]))
    print("Total columns: {}".format(df_total.columns))
    print("Total iflos: {}".format(df_func.shape[0]))

    df_total["DatosHomologados"] = ((df_total["ACT_CHANGE_PM"] == "2") | (df_total["ACT_CHANGE_PM"] == "3")) & ((df_total["ACT_CHANGE_AA"] == "2") | (df_total["ACT_CHANGE_AA"] == "3")) & (df_total["A_objt"] == df_total["E_objt"]) & \
        (df_total["A_pais"] == df_total["E_pais"]) & (df_total["A_invn"] == df_total["E_invn"]) & (df_total["A_fabr"] == df_total["E_fabr"]) & \
        (df_total["A_cost"] == df_total["E_cost"]) & (df_total["A_cent"] == df_total["E_cent"]) & (df_total["A_dane"] == df_total["E_dane"])
    
    df_total.to_excel("total.xlsx")
    return "Notification GEAM Executed:"