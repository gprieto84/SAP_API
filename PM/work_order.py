from config import db, sap_conn
import os

def load(name):
    # Reading the table
    result = sap_conn.call('RFC_READ_TABLE', \
            QUERY_TABLE = 'COAS',
            FIELDS = ['AUFNR','AUART','ERNAM','ERDAT','KTEXT','BUKRS','KOSTV','ASTNR','VAPLZ'], \
            OPTIONS = [{ 'TEXT': "BUKRS EQ 'TRAN' AND AUFNR EQ '" + "000" + name + "'"}], \
            ROWCOUNT = 200, DELIMITER='|')
    print('Entro')

    # Obtaining the fields_value list
    for value in result["DATA"]:
        clean_value = [i.strip(' ') for i in value['WA'].split('|')]

        numorden=clean_value[0]
        claseorden=clean_value[1]
        autor=clean_value[2]
        fecha=clean_value[3]
        textobreve=clean_value[4]
        sociedad=clean_value[5]
        centro=clean_value[6]
        estado=clean_value[7]
        grupo=clean_value[8]

        #Executing the BAPI
        b_result =  sap_conn.call('BAPI_ALM_ORDER_GET_DETAIL', NUMBER=numorden)

        functloc = b_result['ES_HEADER']['FUNCT_LOC'] # Technical location
        equipment = b_result['ES_HEADER']['EQUIPMENT'] # Equipment
        locwkctr = b_result['ES_HEADER']['LOC_WK_CTR'] # Workplace
        startdate = b_result['ES_HEADER']['START_DATE'] # Start date
        finishdate = b_result['ES_HEADER']['FINISH_DATE'] # Finish date
        systatus = b_result['ES_HEADER']['SYS_STATUS'] # status
   
    return "Testing work_order read:" + name
