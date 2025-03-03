#!/usr/bin/env python
import sys
from module_utils.sap_id_sso import sap_sso_login
from module_utils.sap_launchpad_software_center_download_search_fuzzy import *

input_search_file=sys.argv[1]
input_search_file_name_and_version_only=sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]

sap_sso_login(username, password)

query_result = search_software_fuzzy(input_search_file)

if len(query_result) >= 2:
    if '70SWPM' in query_result[0]['Title']:
        print(query_result[-1]['Title'])
    elif any('DBATL' in sublist['Title'] for sublist in query_result):
        for sublist in query_result:
            if sublist['Title'].startswith('DBATL'):
                print(sublist['Title'])
    elif any('_NW_LANG_' in sublist['Description'] for sublist in query_result):
        # Skip _NW_LANG_ files which may have duplicates that are filtered automatically when downloaded
        print('')
    elif any('SYBCTRL' in sublist['Title'] for sublist in query_result):
        for sublist in query_result:
            if sublist['Title'].startswith('SYBCTRL'):
                print(sublist['Title'])
    elif any('SAPEXE_' in sublist['Title'] for sublist in query_result):
        list_sapexe = []
        for sublist in query_result:
            if sublist['Title'].startswith('SAPEXE'):
                list_sapexe.append(int((sublist['Title'].split('-', 1)[0]).split('_', 1)[1]))
        list_sapexe.sort(reverse=True)
        print('SAPEXE_' + str(list_sapexe[0]) + '-' + input_search_file + '.SAR')
    elif any('SAPEXEDB_' in sublist['Title'] for sublist in query_result):
        list_sapexedb = []
        for sublist in query_result:
            if sublist['Title'].startswith('SAPEXEDB'):
                list_sapexedb.append(int((sublist['Title'].split('-', 1)[0]).split('_', 1)[1]))
        list_sapexedb.sort(reverse=True)
        print('SAPEXEDB_' + str(list_sapexedb[0]) + '-' + input_search_file + '.SAR')
    elif any('SMDA' in sublist['Title'] for sublist in query_result):
        input_smda = input_search_file_name_and_version_only[:-2]
        list_smda = []
        for sublist in query_result:
            if sublist['Title'].startswith(input_smda):
                list_smda.append(sublist['Title'])
        list_smda.sort(reverse=True)
        print(list_smda[0])
    elif any('IMDB_CLIENT20' in sublist['Title'] for sublist in query_result):
        input_imdb_client = input_search_file_name_and_version_only[:-2]
        list_imdb_client = []
        for sublist in query_result:
            if sublist['Title'].startswith(input_imdb_client):
                list_imdb_client.append(sublist['Title'])
        list_imdb_client.sort(reverse=True)
        print(list_imdb_client[0])
    elif any('IMDB_AFL' in sublist['Title'] for sublist in query_result):
        input_imdb_afl = input_search_file_name_and_version_only[:-1]
        list_imdb_afl = []
        for sublist in query_result:
            if sublist['Title'].startswith(input_imdb_afl):
                list_imdb_afl.append(sublist['Title'])
        list_imdb_afl.sort(reverse=True)
        print(list_imdb_afl[0])
    elif any('IMDB_LCAPPS' in sublist['Title'] for sublist in query_result):
        input_imdb_lcapps = input_search_file_name_and_version_only[:-1]
        list_imdb_lcapps = []
        for sublist in query_result:
            if sublist['Title'].startswith(input_imdb_lcapps):
                list_imdb_lcapps.append(sublist['Title'])
        list_imdb_lcapps.sort(reverse=True)
        print(list_imdb_lcapps[0])
    elif any('IMDB_SERVER' in sublist['Title'] for sublist in query_result):
        list_imdb_server = []
        for sublist in query_result:
            input_imdb_server = input_search_file_name_and_version_only[:-1]
            if sublist['Title'].startswith(input_imdb_server):
                list_imdb_server.append(sublist['Title'])
        list_imdb_server.sort(reverse=True)
        print(list_imdb_server[0])
        # Match LCAPPS and AFL to new SAP HANA DB Server version
        imdb_server20_existing_prefix = input_search_file_name_and_version_only.split('_')[-1]
        imdb_server20_new_prefix = list_imdb_server[0].split('-')[0]
        imdb_server20_new_prefix2 = imdb_server20_new_prefix.rsplit('_', 1)[0]
        imdb_server20_new_version = imdb_server20_new_prefix2.split('_')[-1]
        imdb_lcapps20_existing_version = "IMDB_LCAPPS_2" + imdb_server20_existing_prefix
        imdb_lcapps20_version = "IMDB_LCAPPS_2" + imdb_server20_new_version
        imdb_lcapps20_query = search_software_fuzzy(imdb_lcapps20_version)
        imdb_lcapps20_result_prefix = imdb_lcapps20_query[0]['Title'].split('-')[0]
        imdb_afl20_existing_version = "IMDB_AFL20_" + imdb_server20_existing_prefix
        imdb_afl20_version = "IMDB_AFL20_" + imdb_server20_new_version
        imdb_afl20_query = search_software_fuzzy(imdb_afl20_version)
        imdb_afl20_result_prefix = imdb_afl20_query[0]['Title'].split('-')[0]
        print(imdb_lcapps20_existing_version + ';' + imdb_lcapps20_result_prefix)
        print(imdb_afl20_existing_version + ';' + imdb_afl20_result_prefix)
    elif any('SAPWEBDISP' in sublist['Title'] for sublist in query_result):
        # As SAP WebDisp file name numbering does not use preceding 0's, manually filter out v7 which is older than v69:
        input_webdisp = input_search_file_name_and_version_only[:-2]
        list_webdisp = []
        for sublist in query_result:
            if sublist['Title'].startswith(input_webdisp) and not sublist['Title'].startswith('SAPWEBDISP_SP_7'):
                list_webdisp.append(sublist['Title'])
        list_webdisp.sort(reverse=True)
        print(list_webdisp[0])
    else:
        print("\nERROR. More than 1 result for " + input_search_file + ", manual intervention required....")
        for item in query_result:
            print('Identified ' + item['Title'] + ' : ' + item['Description'] + ', ' + item['Infotype'],end='\n')
else:
    if len(query_result) == 0:
        print("\nERROR. No result for " + input_search_file + ", manual intervention required....")
    else:
        print(query_result[0]['Title'])
